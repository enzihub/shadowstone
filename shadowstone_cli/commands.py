from pathlib import Path

import typer
import yaml

from shadowstone_cli import __version__
from shadowstone_cli.console import console
from shadowstone_cli.execute import execute_project_creation, make_secrets, step
from shadowstone_cli.models.models import ComponentType
from shadowstone_cli.templates import templates_root
from shadowstone_cli.user_input import collect_project_info, preview_config, update_project_config
from shadowstone_cli.utils import display_name, get_component_class

app = typer.Typer(help="ShadowStone: scaffold a SaaS (Next.js web + FastAPI core).",
                  no_args_is_help=True, add_completion=False)


@app.command()
def create(name: str = typer.Argument(".", help="Project folder name"),
           yes: bool = typer.Option(False, "--yes", "-y", help="Accept the defaults, no questions"),
           demo: bool = typer.Option(False, "--demo", help="Turn on demo mode: local stand-ins for Clerk and Stripe")):
    """Create a new project from the bundled templates."""
    config = collect_project_info(name, defaults=yes)
    if demo:
        config["demo"] = True
    if not preview_config(config, defaults=yes):
        console.print("[warn]Cancelled[/warn]")
        raise typer.Exit(1)
    execute_project_creation(config)


@app.command()
def add(component_type: ComponentType,
        yes: bool = typer.Option(False, "--yes", "-y", help="Accept the defaults, no questions")):
    """Add a web or core component to the project in the current folder."""
    config_file = Path("shadowstone.yaml")
    if not config_file.exists():
        console.print("[red]No shadowstone.yaml here. Run this inside a ShadowStone project.[/red]")
        raise typer.Exit(1)
    config = yaml.safe_load(config_file.read_text())
    comp = get_component_class(component_type.value)(config["project_name"])
    if comp.component_name in config.get("components", {}):
        console.print(f"[warn]{comp.component_name} already exists[/warn]")
        raise typer.Exit(1)
    details = comp.collect_details(defaults=yes)
    config["components"][comp.component_name] = details
    config = update_project_config(config)
    shared = {**config, "display_name": display_name(config["project_name"])}
    secrets = make_secrets()
    other = next((p for p in Path(".").glob(f"{config['project_name']}-*/.env")), None)
    if other:  # reuse the project's existing local Postgres password so both halves match
        for line in other.read_text().splitlines():
            if line.startswith("POSTGRES_PASSWORD=") and line.split("=", 1)[1]:
                pw = line.split("=", 1)[1]
                old = secrets["postgres_password"]
                secrets = {k: v.replace(old, pw) for k, v in secrets.items()}
    count = comp.create(Path("."), details, shared, secrets)
    config_file.write_text(yaml.safe_dump(config, sort_keys=False))
    step(True, comp.component_name, f"{count} files from templates/{component_type.value}")


@app.command()
def templates():
    """Show where the bundled templates live."""
    root = templates_root()
    for kind in ("web", "core"):
        files = sum(1 for p in (root / kind).rglob("*") if p.is_file() and "node_modules" not in p.parts)
        console.print(f"[accent]{kind:5}[/accent] {root / kind}  [dim]{files} files[/dim]")


@app.command()
def version():
    """Print the version."""
    console.print(f"ShadowStone CLI v{__version__}")
