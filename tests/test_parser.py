from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import parser


def test_parse_basic():
    gd_path = Path(__file__).parent / "data" / "basic.gd"
    result = parser.parse_gdscript(str(gd_path))

    assert result["script"]["name"] == "basic"
    assert result["script"]["class_name"] == "Example"
    assert result["script"]["extends"] == "Node"

    assert len(result["signals"]) == 1
    assert result["signals"][0]["name"] == "done"

    assert len(result["enums"]) == 1
    assert result["enums"][0]["name"] == "State"

    assert len(result["consts"]) == 1
    assert result["consts"][0]["name"] == "MAX_SPEED"

    assert len(result["variables"]) == 1
    assert result["variables"][0]["name"] == "name"

    # two functions: _ready and greet
    assert len(result["functions"]) == 2
    assert result["functions"][0]["name"] == "_ready"
    assert result["functions"][1]["name"] == "greet"

    assert len(result["todos"]) == 1
