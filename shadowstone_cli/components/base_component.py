import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

import yaml

from shadowstone_cli.envfile import render_env
from shadowstone_cli.templates import IGNORE, template_dir


class BaseComponent(ABC):
    kind: str = ""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.component_name = f"{project_name}-{self.kind}"

    @abstractmethod
    def collect_details(self, defaults: bool = False) -> Dict[str, Any]:
        """Ask for component settings (or return defaults)."""

    @abstractmethod
    def env_values(self, config: Dict[str, Any], project: Dict[str, Any], secrets: Dict[str, str]) -> Dict[str, str]:
        """Values to write into the component's .env."""

    def customise(self, path: Path, config: Dict[str, Any]) -> None:
        """Component-specific edits after the copy."""

    def create(self, project_path: Path, config: Dict[str, Any], project: Dict[str, Any], secrets: Dict[str, str]) -> int:
        source = template_dir(self.kind)
        target = project_path / self.component_name
        if target.exists():
            raise FileExistsError(f"{target} already exists")
        shutil.copytree(source, target, ignore=shutil.ignore_patterns(*IGNORE))

        example = target / ".env.example"
        if example.exists():
            (target / ".env").write_text(render_env(example, self.env_values(config, project, secrets)))

        with (target / "shadowstone.component.yaml").open("w") as f:
            yaml.safe_dump({"component": self.component_name, "type": self.kind, **config}, f, sort_keys=False)

        self.customise(target, config)
        return sum(1 for p in target.rglob("*") if p.is_file())
