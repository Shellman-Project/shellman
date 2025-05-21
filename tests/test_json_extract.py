from click.testing import CliRunner
from shellman.commands.json_extract import cli
from pathlib import Path
import json


def create_json_file(path: Path):
    content = {
        "items": [
            {"id": 1, "name": "alpha", "status": "ok"},
            {"id": 2, "name": "beta", "status": "ERROR"},
            {"id": 3, "name": "gamma", "status": "ok"}
        ]
    }
    path.write_text(json.dumps(content), encoding="utf-8")


def test_extract_path(tmp_path):
    f = tmp_path / "data.json"
    create_json_file(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--path", "items"])
    assert result.exit_code == 0
    assert "\"name\": \"alpha\"" in result.output
    assert "\"id\": 3" in result.output


def test_filter_by_key(tmp_path):
    f = tmp_path / "data.json"
    create_json_file(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--path", "items", "--filter", "status=ERROR"])
    assert result.exit_code == 0
    assert "\"name\": \"beta\"" in result.output
    assert "\"name\": \"alpha\"" not in result.output


def test_field_selection(tmp_path):
    f = tmp_path / "data.json"
    create_json_file(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--path", "items", "--fields", "id,name"])
    assert result.exit_code == 0
    assert "\"id\": 1" in result.output
    assert "\"status\"" not in result.output


def test_output_file(tmp_path):
    f = tmp_path / "data.json"
    out = tmp_path / "result.json"
    create_json_file(f)

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--path", "items", "--fields", "id", "--output", str(out)])
    assert result.exit_code == 0
    content = out.read_text()
    assert "\"id\": 1" in content
    assert out.exists()


def test_invalid_path(tmp_path):
    f = tmp_path / "data.json"
    f.write_text(json.dumps({"data": []}), encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(cli, [str(f), "--path", "invalid"])
    assert result.exit_code != 0
