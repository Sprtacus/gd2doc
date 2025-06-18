from pathlib import Path
import sys
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.cli import main


def test_cli_recursive_option(tmp_path):
    source = tmp_path / "src"
    output = tmp_path / "out"
    sub = source / "sub"
    sub.mkdir(parents=True)

    data_file = Path(__file__).parent / "data" / "basic.gd"
    nested_file = Path(__file__).parent / "data" / "sub" / "nested.gd"
    (source / "basic.gd").write_text(data_file.read_text(), encoding="utf-8")
    (sub / "nested.gd").write_text(nested_file.read_text(), encoding="utf-8")

    runner = CliRunner()
    # without recursion only top level file should be processed
    result = runner.invoke(main, [str(source), "-o", str(output)])
    assert result.exit_code == 0
    assert (output / "basic.md").exists()
    assert not (output / "sub" / "nested.md").exists()

    output2 = tmp_path / "out_rec"
    result = runner.invoke(main, [str(source), "-o", str(output2), "--recursive"])
    assert result.exit_code == 0
    assert (output2 / "basic.md").exists()
    assert (output2 / "sub" / "nested.md").exists()

