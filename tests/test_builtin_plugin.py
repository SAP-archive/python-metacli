import click
import json
import pathlib
import jsondiff
import os
from click.testing import CliRunner
import pytest


def test_builtin_schema(monkeypatch, root):
    runner = CliRunner()

    result = runner.invoke(root)
    assert result.exit_code == 0

    # test schema
    result = runner.invoke(root, ['dog', '--help'])
    assert result.exit_code == 0
    assert """schema  Generate cmd structure json and get help info""" in result.output

    result = runner.invoke(root, ['dog', 'schema'])
    assert result.exit_code == 0
    assert """Generate help info in schema.json""" in result.output

    # compare result and the template
    base = pathlib.Path(__file__).resolve().parent
    with open(str(base) + '/templates/schema.json') as json_file:
        template = json.load(json_file)

    result_path = os.getcwd() + "/schema.json"
    with open(result_path) as json_file:
        result = json.load(json_file)

    # compare the result and template with order
    result = jsondiff.diff(result, template)
    assert len(result) == 0

    # clean up
    if pathlib.Path(result_path).exists():
        os.remove(result_path)


def test_builtin_shell(root):
    runner = CliRunner()

    result = runner.invoke(root)
    assert result.exit_code == 0

    # test shell
    result = runner.invoke(root, ['dog', 'shell', '--help'])
    assert result.exit_code == 0
    assert """Shell""" in result.output


if __name__ == '__main__':
    pytest.main()

