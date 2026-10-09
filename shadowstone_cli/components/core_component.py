import os
from pathlib import Path
from typing import Any, Dict

from beaupy import prompt

from shadowstone_cli.console import console
from .base_component import BaseComponent


class CoreComponent(BaseComponent):
    kind = "core"

    def collect_details(self, defaults: bool = False) -> Dict[str, Any]:
        if defaults:
            return {"api_port": int(os.getenv("SS_API_PORT", "8000"))}
        console.print(f"\n[bold]API ({self.component_name})[/bold]")
        port = prompt("Port for the FastAPI server:", initial_value="8000") or "8000"
        return {"api_port": int(port)}

    def env_values(self, config, project, secrets) -> Dict[str, str]:
        values = {
            "ENVIRONMENT": "development",
            "APP_NAME": project["display_name"],
            "PORT": str(config.get("api_port", 8000)),
            "REDIS_URL": f"redis://localhost:{secrets['redis_port']}/0",
            "REDIS_PORT": secrets["redis_port"],
            "CELERY_BROKER_URL": f"redis://localhost:{secrets['redis_port']}/0",
            "CELERY_RESULT_BACKEND": f"redis://localhost:{secrets['redis_port']}/0",
        }
        web = project.get("components", {}).get(f"{self.project_name}-web")
        if web:
            values["APP_URL"] = f"http://localhost:{web.get('port', 3000)}"
        if project["database"]["provider"] == "postgres-docker":
            values["DATABASE_URL"] = secrets["database_url_core"]
        return values
