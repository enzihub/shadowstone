"""Find the bundled templates (templates/web, templates/core)."""
import os
from pathlib import Path

IGNORE = ("node_modules", ".next", "__pycache__", ".venv", "venv", ".pytest_cache",
          ".env", ".env.local", ".env.development", ".env.production", "*.pyc", ".DS_Store")


def templates_root() -> Path:
    override = os.getenv("SHADOWSTONE_TEMPLATES")
    candidates = [Path(override)] if override else []
    here = Path(__file__).resolve().parent
    candidates += [here / "_templates", here.parent / "templates"]
    for c in candidates:
        if (c / "web").is_dir() and (c / "core").is_dir():
            return c
    raise FileNotFoundError(
        "Could not find the bundled templates. Set SHADOWSTONE_TEMPLATES to the repo's templates/ folder."
    )


def template_dir(kind: str) -> Path:
    return templates_root() / kind
