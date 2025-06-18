"""Command line interface for gd2doc."""

from __future__ import annotations

from pathlib import Path
from typing import List
import shutil

import click

from . import parser, generator


def _collect_gd_files(root: Path, recursive: bool) -> List[Path]:
    """Return a list of ``.gd`` files found under ``root``."""
    if root.is_file() and root.suffix == ".gd":
        return [root]

    if not root.is_dir():
        return []

    pattern = "**/*.gd" if recursive else "*.gd"
    return [p for p in root.glob(pattern)]


@click.command()
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, path_type=Path),
    required=True,
    help="Directory to write the generated Markdown files to.",
)
@click.option(
    "--recursive/--no-recursive",
    "-r",
    default=False,
    help="Search SOURCE recursively for .gd files.",
)
@click.option(
    "--clean/--no-clean",
    default=False,
    help="Delete OUTPUT_DIR before generating new documentation.",
)
def main(source: Path, output_dir: Path, recursive: bool, clean: bool) -> None:
    """Generate documentation for all ``.gd`` files under ``SOURCE``."""

    gd_files = _collect_gd_files(source, recursive)
    if not gd_files:
        click.echo("No .gd files found.")
        return

    if clean and output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    base = source if source.is_dir() else source.parent
    for gd_file in gd_files:
        data = parser.parse_gdscript(str(gd_file))
        rel = gd_file.relative_to(base)
        target = (output_dir / rel).with_suffix(".md")
        generator.generate_markdown(data, str(target))
        click.echo(f"Generated {target.relative_to(output_dir)}")


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()

