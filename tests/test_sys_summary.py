from click.testing import CliRunner

from shellman.commands.sys_summary import cli


def test_sys_summary_output_contains_sections():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0
    output = result.output

    assert "System Summary" in output
    assert "OS & Host" in output
    assert "Shell" in output
    assert "Tools" in output
    assert "Memory" in output
    assert "Uptime & Load" in output
    assert "Disks" in output
    assert "Network" in output
    assert "Packages" in output
