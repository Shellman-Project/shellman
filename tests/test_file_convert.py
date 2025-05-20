import json
import yaml
import toml
from click.testing import CliRunner
from shellman.commands.file_convert import cli
from pathlib import Path

def test_json_to_yaml(tmp_path):
    source = tmp_path / "example.json"
    source.write_text(json.dumps({"key": "value", "num": 1}))
    
    runner = CliRunner()
    result = runner.invoke(cli, [str(source), "--from", "json", "--to", "yaml"])
    
    assert result.exit_code == 0
    output = yaml.safe_load(result.output)
    assert output["key"] == "value"
    assert output["num"] == 1

def test_toml_to_json_pretty(tmp_path):
    source = tmp_path / "example.toml"
    source.write_text("[section]\nvalue = \"test\"")

    runner = CliRunner()
    result = runner.invoke(cli, [str(source), "--from", "toml", "--to", "json", "--pretty"])
    
    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output["section"]["value"] == "test"

def test_invalid_format(tmp_path):
    file = tmp_path / "file.unknown"
    file.write_text("some data")

    runner = CliRunner()
    result = runner.invoke(cli, [str(file), "--from", "unknown", "--to", "json"])

    assert result.exit_code != 0
    assert "Invalid value for '--from'" in result.output
    assert "'unknown' is not one of 'json', 'yaml', 'toml'" in result.output


def test_output_to_file(tmp_path):
    source = tmp_path / "config.yaml"
    source.write_text("app:\n  debug: true")

    output = tmp_path / "converted.json"
    
    runner = CliRunner()
    result = runner.invoke(cli, [
        str(source), "--from", "yaml", "--to", "json", "--output", str(output)
    ])

    assert result.exit_code == 0
    assert output.exists()
    with output.open() as f:
        data = json.load(f)
        assert data["app"]["debug"] is True
