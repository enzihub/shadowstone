import os
import json
from pathlib import Path
from typing import Any, Dict

from beaupy import prompt

from shadowstone_cli.console import console
from .base_component import BaseComponent


class WebComponent(BaseComponent):
    kind = "web"

    def collect_details(self, defaults: bool = False) -> Dict[str, Any]:
        if defaults:
            return {"port": int(os.getenv("SS_WEB_PORT", "3000"))}
        console.print(f"\n[bold]Web app ({self.component_name})[/bold]")
        port = prompt("Port for the Next.js dev server:", initial_value="3000") or "3000"
        return {"port": int(port)}

    def env_values(self, config, project, secrets) -> Dict[str, str]:
        port = config.get("port", 3000)
        core = project.get("components", {}).get(f"{self.project_name}-core")
        values = {
            "SITE_URL": f"http://localhost:{port}",
            "NEXT_PUBLIC_SITE_URL": f"http://localhost:{port}",
            "NEXT_PUBLIC_APP_NAME": project["display_name"],
        }
        plans = []
        for tier in project.get("billing", {}).get("tiers", []) if project.get("billing", {}).get("enabled") else []:
            for price in tier.get("prices", []):
                interval = {"monthly": "month", "yearly": "year"}[price["interval"]]
                plans.append({"id": f"price_demo_{tier['name'].lower()}_{interval}", "product": tier["name"],
                              "description": f"{tier['name']} plan", "amount": int(round(price["amount"] * 100)),
                              "interval": interval})
        values["DEMO_STRIPE_PLANS"] = "'" + json.dumps(plans, separators=(",", ":")) + "'"
        values["NEXT_PUBLIC_DEMO_MODE"] = "1" if project.get("demo") else ""
        if core:
            values["NEXT_PUBLIC_CORE_API_URL"] = f"http://localhost:{core.get('api_port', 8000)}"
        if project["database"]["provider"] == "postgres-docker":
            values.update({
                "POSTGRES_PASSWORD": secrets["postgres_password"],
                "PG_CONNECTION_STRING": secrets["pg_proxy_url"],
                "DATABASE_URL": secrets["database_url_web"],
                "NEON_HTTP_ENDPOINT": f"http://db.localtest.me:{secrets['neon_port']}/sql",
                "POSTGRES_PORT": secrets["postgres_port"],
                "NEON_PROXY_PORT": secrets["neon_port"],
            })
        return values

    def customise(self, path: Path, config: Dict[str, Any]) -> None:
        pkg = path / "package.json"
        data = json.loads(pkg.read_text())
        data["name"] = self.component_name
        port = config.get("port", 3000)
        data["scripts"]["dev"] = f"next dev -p {port}"
        data["scripts"]["start"] = f"next start -p {port}"
        data["scripts"]["stripe:listen"] = f"stripe listen --forward-to=localhost:{port}/api/webhooks/stripe"
        pkg.write_text(json.dumps(data, indent=2) + "\n")
