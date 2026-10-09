"""Tiny .env helpers: read .env.example, fill known keys, keep comments and order."""
from pathlib import Path
from typing import Dict


def render_env(example: Path, values: Dict[str, str]) -> str:
    seen = set()
    out = []
    for line in example.read_text().splitlines():
        key = line.split("=", 1)[0].strip() if "=" in line and not line.lstrip().startswith("#") else None
        if key and key in values:
            out.append(f"{key}={values[key]}")
            seen.add(key)
        else:
            out.append(line.rstrip())
    extra = [k for k in values if k not in seen]
    if extra:
        out.append("")
        out.append("# Added by ShadowStone")
        out += [f"{k}={values[k]}" for k in extra]
    return "\n".join(out) + "\n"
