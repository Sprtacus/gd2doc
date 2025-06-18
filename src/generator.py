"""Markdown documentation generator using Jinja2 templates."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from jinja2 import Environment, FileSystemLoader
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    Environment = None  # type: ignore
    FileSystemLoader = None  # type: ignore


def generate_markdown(
    data: Dict[str, Any], output_path: str, template_dir: Optional[str] = None
) -> str:
    """Generate a Markdown file from parsed GDScript data.

    Parameters
    ----------
    data:
        Parsed representation of a GDScript file as returned by ``parser.parse_gdscript``.
    output_path:
        Target path where the rendered Markdown file should be written.
    template_dir:
        Optional directory containing the ``doc.md.j2`` template.  If not
        supplied the ``templates`` directory next to this file is used.

    Returns
    -------
    str
        The rendered Markdown content.
    """

    if Environment is None:
        # Minimal fallback when Jinja2 is unavailable
        script = data.get("script", {})
        markdown = f"# {script.get('name', '')}\n"
    else:
        tdir = template_dir or os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(
            loader=FileSystemLoader(tdir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.get_template("doc.md.j2")
        markdown = template.render(**data)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(markdown, encoding="utf-8")

    return markdown

