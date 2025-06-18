"""Markdown documentation generator using Jinja2 templates."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional, List

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


def generate_indexes(gd_files: List[Path], base: Path, output_dir: Path) -> None:
    """Generate ``index.md`` files for all directories.

    Parameters
    ----------
    gd_files:
        Collection of processed ``.gd`` files.
    base:
        Base directory relative to which ``gd_files`` are located.
    output_dir:
        Root directory for the generated Markdown files.
    """

    rel_files = [p.relative_to(base) for p in gd_files]
    directories = {Path(".")}
    for rel in rel_files:
        directories.update(rel.parents)

    # sort so parents are created before children
    for directory in sorted(directories, key=lambda d: (len(d.parts), str(d))):
        subdirs = sorted({d.name for d in directories if d.parent == directory})
        scripts = sorted(
            [p.with_suffix(".md").name for p in rel_files if p.parent == directory]
        )

        title = directory.name if directory != Path(".") else "Index"
        lines = [f"# {title}"]
        if subdirs:
            lines.append("## Ordner")
            for sd in subdirs:
                lines.append(f"- [{sd}]({sd}/index.md)")
        if scripts:
            lines.append("## Skripte")
            for s in scripts:
                lines.append(f"- [{Path(s).stem}]({s})")

        content = "\n".join(lines) + "\n"
        out_path = output_dir / directory / "index.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")


def _nav_lines(directory: Path, root: Path, indent: int = 0) -> List[str]:
    """Return YAML formatted nav lines for ``directory``."""

    lines: List[str] = []

    for subdir in sorted([p for p in directory.iterdir() if p.is_dir()]):
        lines.append(" " * indent + f"- {subdir.name}:")
        lines.append(
            " " * (indent + 2)
            + f"- Overview: {subdir.relative_to(root) / 'index.md'}"
        )
        lines.extend(_nav_lines(subdir, root, indent + 2))

    for script in sorted([p for p in directory.glob("*.md") if p.name != "index.md"]):
        lines.append(
            " " * indent + f"- {script.stem}: {script.relative_to(root)}"
        )

    return lines


def generate_mkdocs_yml(project_root: Path, docs_dir: Path) -> None:
    """Create a ``mkdocs.yml`` next to ``project_root`` using ``docs_dir``."""

    try:
        docs_rel = docs_dir.relative_to(project_root)
    except ValueError:
        docs_rel = Path(os.path.relpath(docs_dir, project_root))

    lines = [f"site_name: {project_root.name}", "nav:", "  - Home: index.md", "  - Codebase:"]
    lines.extend(["    " + l for l in _nav_lines(docs_dir, docs_dir)])
    lines.extend(
        [
            "theme:",
            "  name: readthedocs",
            f"docs_dir: {docs_rel}",
            "site_dir: site",
            "markdown_extensions:",
            "  - admonition",
            "  - toc:",
            "      permalink: true",
            "plugins:",
            "  - search",
            "",
        ]
    )

    (project_root / "mkdocs.yml").write_text("\n".join(lines), encoding="utf-8")

