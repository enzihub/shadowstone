import datetime
import os
from typing import Type

import typer
from rich.panel import Panel

from shadowstone_cli import __version__
from shadowstone_cli.console import console
from shadowstone_cli.components.base_component import BaseComponent
from shadowstone_cli.components.core_component import CoreComponent
from shadowstone_cli.components.web_component import WebComponent


def print_welcome():
    console.print(Panel.fit(
        "[accent]ShadowStone[/accent]  scaffold a SaaS: Next.js web + FastAPI core",
        subtitle=f"v{__version__}", border_style="#8b5cf6"))


def get_component_class(component_type: str) -> Type[BaseComponent]:
    return {"web": WebComponent, "core": CoreComponent}[component_type]


def get_timestamp() -> str:
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def display_name(slug: str) -> str:
    return " ".join(p.capitalize() for p in slug.replace("_", "-").split("-") if p)


def get_env_var(var_name: str, message: str, is_secret: bool = False, required: bool = True) -> str:
    """Return an environment variable, or ask for it (optional ones may be left blank)."""
    value = os.getenv(var_name)
    if not value and required:
        value = typer.prompt(message, type=str, hide_input=is_secret)
        os.environ[var_name] = value
    return value or ""
