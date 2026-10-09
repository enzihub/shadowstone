import os
import secrets
import subprocess
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv
from rich.panel import Panel

from shadowstone_cli.console import console
from shadowstone_cli.models.config import ProjectConfig
from shadowstone_cli.utils import display_name, get_component_class

load_dotenv()


def local_ports() -> Dict[str, int]:
    """Host ports for the local containers. Override with SS_POSTGRES_PORT, SS_NEON_PORT, SS_REDIS_PORT."""
    return {"postgres": int(os.getenv("SS_POSTGRES_PORT", "5432")),
            "neon": int(os.getenv("SS_NEON_PORT", "4444")),
            "redis": int(os.getenv("SS_REDIS_PORT", "6379"))}


def make_secrets() -> Dict[str, str]:
    """A fresh local Postgres password per project, and the URLs that use it."""
    pw = secrets.token_hex(12)
    scheme, user = "postgres", "postgres"
    ports = local_ports()
    return {
        "postgres_password": pw,
        "postgres_port": str(ports["postgres"]),
        "neon_port": str(ports["neon"]),
        "redis_port": str(ports["redis"]),
        "pg_proxy_url": f"{scheme}://{user}:{pw}@postgres:5432/main",
        "database_url_web": f"{scheme}://{user}:{pw}@db.localtest.me:{ports['postgres']}/main",
        "database_url_core": f"{scheme}ql+psycopg2://{user}:{pw}@localhost:{ports['postgres']}/main",
    }


def step(ok: bool, text: str, note: str = "") -> None:
    mark = "[ok]✔[/ok]" if ok else "[warn]![/warn]"
    console.print(f" {mark} {text}" + (f"  [dim]{note}[/dim]" if note else ""))


def setup_billing(config: ProjectConfig) -> Dict[str, Any]:
    if not config.billing.enabled:
        return {}
    key = os.getenv("STRIPE_SECRET_KEY", "")
    tiers = ", ".join(t.name for t in config.billing.tiers)
    if not key:
        step(False, f"Stripe tiers saved ({tiers})", "set STRIPE_SECRET_KEY to create them in Stripe")
        return {}
    import stripe

    stripe.api_key = key
    created = {}
    for tier in config.billing.tiers:
        product = stripe.Product.create(name=tier.name, description=f"{tier.name} plan",
                                        metadata={"app_code": config.project_name})
        prices = []
        for p in tier.prices:
            price = stripe.Price.create(product=product.id, unit_amount=int(p.amount * 100), currency="usd",
                                        recurring={"interval": {"monthly": "month", "yearly": "year"}[p.interval]})
            prices.append({"id": price.id, "amount": p.amount, "interval": p.interval})
        created[tier.name] = {"product_id": product.id, "prices": prices}
    step(True, f"Created {len(created)} Stripe products", "test mode" if key.startswith("sk_test") else "")
    return created


def setup_deployment(config: ProjectConfig) -> None:
    if not config.deployment.enabled:
        return
    url, token = os.getenv("COOLIFY_URL", ""), os.getenv("COOLIFY_API_TOKEN", "")
    if not (url and token):
        step(False, "Coolify skipped", "set COOLIFY_URL and COOLIFY_API_TOKEN")
        return
    import requests

    r = requests.post(f"{url.rstrip('/')}/api/v1/projects", timeout=20,
                      headers={"Authorization": f"Bearer {token}"},
                      json={"name": config.project_name, "description": config.deployment.description})
    step(r.ok, "Created Coolify project" if r.ok else f"Coolify returned HTTP {r.status_code}")


def git_init(path: Path) -> bool:
    try:
        subprocess.run(["git", "init", "-q", "-b", "main", str(path)], check=True, capture_output=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def next_steps(config: ProjectConfig) -> None:
    lines = [f"[bold]cd {config.project_name}[/bold]"]
    web, core = f"{config.project_name}-web", f"{config.project_name}-core"
    if web in config.components:
        port = config.components[web].get("port", 3000)
        lines += ["", f"[accent]web[/accent]   cd {web}",
                  "      docker compose up -d      [dim]# Postgres + local Neon HTTP proxy[/dim]",
                  "      npm install && npm run db:migrate",
                  f"      npm run dev               [dim]# http://localhost:{port}[/dim]"]
    if core in config.components:
        port = config.components[core].get("api_port", 8000)
        lines += ["", f"[accent]core[/accent]  cd {core}",
                  "      docker compose up -d redis",
                  f"      uv run uvicorn main:app --reload --port {port}   [dim]# /docs[/dim]"]
    if config.oauth.enabled:
        lines += ["", f"[dim]Clerk: create an app with {', '.join(config.oauth.providers)} sign-in and paste its keys into .env[/dim]"]
    console.print(Panel("\n".join(lines), title="Next steps", border_style="#8b5cf6", expand=False))


def execute_project_creation(raw: Dict[str, Any], base: Path = Path(".")) -> Path:
    config = ProjectConfig.from_dict(raw)
    project_path = base / config.project_name
    project_path.mkdir(parents=True, exist_ok=False)
    step(True, f"Created {project_path}/")

    shared = {**config.to_dict(), "display_name": display_name(config.project_name)}
    keys = make_secrets()
    for name, cfg in config.components.items():
        kind = name.rsplit("-", 1)[-1]
        count = get_component_class(kind)(config.project_name).create(project_path, cfg, shared, keys)
        step(True, f"{name}", f"{count} files from templates/{kind}")
    if config.database.provider == "postgres-docker":
        step(True, "Wrote .env files", "fresh local Postgres password, never committed")
    else:
        step(True, "Wrote .env files", "add your DATABASE_URL")

    stripe_ids = setup_billing(config)
    setup_deployment(config)

    out = config.to_dict()
    if stripe_ids:
        out["billing"]["stripe"] = stripe_ids
    with (project_path / "shadowstone.yaml").open("w") as f:
        yaml.safe_dump(out, f, sort_keys=False)
    (project_path / ".gitignore").write_text(".env\n.env.*\n!.env.example\nnode_modules/\n.next/\n__pycache__/\n.venv/\n")
    (project_path / "README.md").write_text(
        f"# {display_name(config.project_name)}\n\nScaffolded with ShadowStone.\n\n"
        + "\n".join(f"- `{c}/`" for c in config.components) + "\n")
    step(git_init(project_path), "git init", "branch main")
    console.print(f"\n[ok]Done.[/ok] {display_name(config.project_name)} is ready.\n")
    next_steps(config)
    return project_path
