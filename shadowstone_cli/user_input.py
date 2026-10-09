from typing import Any, Dict, List

import yaml
from beaupy import confirm, prompt, select, select_multiple
from rich.syntax import Syntax

from shadowstone_cli.console import console
from shadowstone_cli.models.models import ComponentType
from shadowstone_cli.utils import display_name, get_component_class, get_timestamp, print_welcome

STYLE = dict(cursor_style="#8b5cf6")
TICK = dict(cursor_style="#8b5cf6", tick_style="#8b5cf6")


def ask_components(project_name: str, defaults: bool) -> Dict[str, Dict[str, Any]]:
    kinds = [ComponentType.web, ComponentType.core]
    if defaults:
        chosen = kinds
    else:
        console.print("\n[bold]Which parts do you want?[/bold]")
        labels = [f"{project_name}-web   Next.js 14 + Clerk + Stripe + Drizzle",
                  f"{project_name}-core  FastAPI + Celery + Redis + SQLAlchemy"]
        picked = select_multiple(labels, ticked_indices=[0, 1], return_indices=True, **TICK)
        chosen = [kinds[i] for i in picked]
    out = {}
    for kind in chosen:
        comp = get_component_class(kind.value)(project_name)
        out[comp.component_name] = comp.collect_details(defaults)
    return out


def ask_oauth(defaults: bool) -> List[str]:
    if defaults:
        return ["Google", "GitHub"]
    console.print("\n[bold]Sign-in providers to enable in Clerk:[/bold]")
    return select_multiple(["Google", "GitHub", "Microsoft", "Slack"], ticked_indices=[0, 1], **TICK)


def ask_database(defaults: bool) -> str:
    if defaults:
        return "postgres-docker"
    console.print("\n[bold]Database:[/bold]")
    options = ["Postgres in Docker (local, generated password)", "I will bring my own DATABASE_URL"]
    return ["postgres-docker", "external"][select(options, return_index=True, **STYLE)]


def ask_billing(defaults: bool) -> Dict[str, Any]:
    if defaults:
        return {"enabled": True, "provider": "stripe", "tiers": [
            {"name": "Starter", "prices": [{"amount": 9.0, "interval": "monthly"}, {"amount": 90.0, "interval": "yearly"}]},
            {"name": "Pro", "prices": [{"amount": 29.0, "interval": "monthly"}, {"amount": 290.0, "interval": "yearly"}]},
        ]}
    console.print("\n[bold]Set up Stripe subscription tiers?[/bold]")
    if not confirm("", default_is_yes=True, **STYLE):
        return {"enabled": False}
    tiers = []
    count = prompt("How many tiers?", initial_value="2") or "2"
    for i in range(max(1, int(count))):
        name = prompt(f"Tier {i + 1} name:") or f"Tier {i + 1}"
        prices = []
        for interval in ("monthly", "yearly"):
            amount = prompt(f"{name} {interval} price (USD):")
            if amount:
                prices.append({"amount": float(amount), "interval": interval})
        tiers.append({"name": name, "prices": prices})
    return {"enabled": True, "provider": "stripe", "tiers": tiers}


def ask_deployment(project_name: str, defaults: bool) -> Dict[str, Any]:
    if defaults:
        return {"enabled": False, "provider": "coolify", "description": ""}
    console.print("\n[bold]Create a Coolify project for deployment?[/bold]")
    enabled = confirm("", default_is_yes=False, **STYLE)
    return {"enabled": bool(enabled), "provider": "coolify", "description": f"Deployment for {project_name}"}


def collect_project_info(name: str, defaults: bool = False) -> Dict[str, Any]:
    print_welcome()
    if not name or name == ".":
        name = "my-saas" if defaults else (prompt("Project name:", initial_value="my-saas") or "my-saas")
    name = name.strip().lower().replace(" ", "-")
    ts = get_timestamp()
    return {
        "project_name": name,
        "components": ask_components(name, defaults),
        "oauth": {"enabled": True, "providers": ask_oauth(defaults)},
        "database": {"provider": ask_database(defaults)},
        "billing": ask_billing(defaults),
        "deployment": ask_deployment(name, defaults),
        "created_at": ts,
        "updated_at": ts,
    }


def preview_config(config: Dict[str, Any], defaults: bool = False) -> bool:
    console.print("\n[bold]shadowstone.yaml[/bold]")
    console.print(Syntax(yaml.safe_dump(config, sort_keys=False), "yaml", theme="monokai", background_color="default"))
    if defaults:
        return True
    return select(["Create project", "Cancel"], return_index=True, **STYLE) == 0


def update_project_config(config: Dict[str, Any]) -> Dict[str, Any]:
    config["updated_at"] = get_timestamp()
    return config
