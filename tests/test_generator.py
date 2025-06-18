from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import generator, parser


def test_generate_markdown(tmp_path):
    gd_path = Path(__file__).parent / "data" / "basic.gd"
    parsed = parser.parse_gdscript(str(gd_path))

    output = tmp_path / "basic.md"
    generator.generate_markdown(parsed, str(output))

    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert "# basic" in content

