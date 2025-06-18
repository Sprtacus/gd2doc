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

def test_parse_advanced():
    gd_path = Path(__file__).parent / "data" / "advanced.gd"
    result = parser.parse_gdscript(str(gd_path))

    script = result["script"]
    assert script["name"] == "advanced"
    assert script["class_name"] == "FullExample"
    assert script["extends"] == "Node2D"
    assert script["short_description"] == "A script demonstrating full parsing."
    assert script["description"] == "A script demonstrating full parsing.\nContains multiple features."

    # signal with argument and description
    assert len(result["signals"]) == 1
    sig = result["signals"][0]
    assert sig["name"] == "something"
    assert sig["description"] == "Emitted when something happens"
    assert len(sig["args"]) == 1
    assert sig["args"][0].name == "value"

    # enum with items and description
    assert len(result["enums"]) == 1
    enum = result["enums"][0]
    assert enum["name"] == "Action"
    assert enum["description"] == "Example action enum"
    assert [item["name"] for item in enum["items"]] == ["RUN", "JUMP", "CROUCH"]
    assert enum["items"][1]["value"] == 3

    # constant with description
    assert len(result["consts"]) == 1
    const = result["consts"][0]
    assert const["name"] == "PI"
    assert const["value"] == "3.14"
    assert const["description"] == "Important constant"

    # variable with type, default and description
    assert len(result["variables"]) == 1
    var = result["variables"][0]
    assert var["name"] == "score"
    assert var["type"] == "int"
    assert var["default"] == "0"
    assert var["description"] == "The player's score"

    # functions with params, return types and descriptions
    assert len(result["functions"]) == 2
    proc = result["functions"][0]
    assert proc["name"] == "_process"
    assert proc["description"] == "Called every frame"
    assert len(proc["params"]) == 1
    assert proc["params"][0]["name"] == "delta"
    assert proc["params"][0]["type"] == "float"
    assert proc["returns"]["type"] == "void"

    add_func = result["functions"][1]
    assert add_func["name"] == "add"
    assert add_func["description"] == "Adds a value to score"
    assert len(add_func["params"]) == 1
    assert add_func["params"][0]["name"] == "value"
    assert add_func["params"][0]["type"] == "int"
    assert add_func["params"][0]["default"] == "1"
    assert add_func["returns"]["type"] == "int"

    # todos collected
    assert result["todos"] == [
        ": top header todo",
        ": constant to check",
        ": final todo",
    ]
