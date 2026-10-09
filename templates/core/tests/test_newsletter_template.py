from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).parent.parent / "templates"


def render(**data) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True)
    return env.get_template("newsletter.html").render(**data)


def test_newsletter_template_renders():
    html = render(
        timestamp=datetime(2025, 3, 14).strftime("%B %d, %Y"),
        logo_data="https://example.com/logo.png",
        app_url="https://example.com",
        summary="<div class='text'>The mobile beta reached 40 testers.</div>",
        prep_for="Ada Park",
        prep_by="Acme Notes",
    )
    assert "Ada Park" in html
    assert "https://example.com/settings" in html
