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


def test_cli_clean_option(tmp_path):
    source = tmp_path / "src"
    source.mkdir()
    output = tmp_path / "docs"
    output.mkdir()

    data_file = Path(__file__).parent / "data" / "basic.gd"
    (source / "basic.gd").write_text(data_file.read_text(), encoding="utf-8")

    leftover = output / "old.md"
    leftover.write_text("old", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, [str(source), "-o", str(output), "--clean"])
    assert result.exit_code == 0
    assert (output / "basic.md").exists()
    assert not leftover.exists()


def test_cli_generates_indexes(tmp_path):
    source = tmp_path / "src"
    output = tmp_path / "out"
    sub = source / "sub"
    sub.mkdir(parents=True)

    data_file = Path(__file__).parent / "data" / "basic.gd"
    nested_file = Path(__file__).parent / "data" / "sub" / "nested.gd"
    (source / "basic.gd").write_text(data_file.read_text(), encoding="utf-8")
    (sub / "nested.gd").write_text(nested_file.read_text(), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, [str(source), "-o", str(output), "--recursive"])
    assert result.exit_code == 0

    root_index = output / "index.md"
    assert root_index.exists()
    content_root = root_index.read_text(encoding="utf-8")
    assert "basic.md" in content_root
    assert "sub/index.md" in content_root

    sub_index = output / "sub" / "index.md"
    assert sub_index.exists()
    content_sub = sub_index.read_text(encoding="utf-8")
    assert "nested.md" in content_sub


def test_cli_indexes_intermediate_dirs(tmp_path):
    source = tmp_path / "src"
    output = tmp_path / "out"
    deep = source / "a" / "b"
    deep.mkdir(parents=True)

    data_file = Path(__file__).parent / "data" / "basic.gd"
    (deep / "deep.gd").write_text(data_file.read_text(), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(main, [str(source), "-o", str(output), "-r"])
    assert result.exit_code == 0

    assert (output / "index.md").exists()
    assert (output / "a" / "index.md").exists()
    assert (output / "a" / "b" / "index.md").exists()

    root_content = (output / "index.md").read_text(encoding="utf-8")
    assert "a/index.md" in root_content
    a_content = (output / "a" / "index.md").read_text(encoding="utf-8")
    assert "b/index.md" in a_content
    b_content = (output / "a" / "b" / "index.md").read_text(encoding="utf-8")
    assert "deep.md" in b_content
