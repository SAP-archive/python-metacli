import pytest
import click
import json
import pathlib
import jsondiff
import os
from metacli.decorators import loadPlugin
from click.testing import CliRunner


@loadPlugin(json_file="./plugin_commands_test.json", base_path=__file__)
@click.group()
@click.pass_context
def root_plugin(ctx):
    """root plugin"""


def test_builtin_schema():
    runner = CliRunner()

    result = runner.invoke(root_plugin)
    assert result.exit_code == 0

    # test schema
    result = runner.invoke(root_plugin, ['dog', '--help'])
    assert result.exit_code == 0
    assert """schema  Generate cmd structure json and get help info""" in result.output

    result = runner.invoke(root_plugin, ['dog', 'schema'])
    assert result.exit_code == 0
    assert """Generate help info in schema.json""" in result.output

    # compare result and the template
    with open('templates/schema.json') as json_file:
        template = json.load(json_file)

    # get example/dog path
    base = pathlib.Path(__file__).resolve().parent
    result_path = str((base / pathlib.Path("../example/dog/schema.json")).resolve())
    with open(result_path) as json_file:
        result = json.load(json_file)

    # compare the result and template with order
    result = jsondiff.diff(result, template)
    assert len(result) == 0

    # clean up
    if pathlib.Path('schema.json').exists():
        os.remove("schema.json")


def test_builtin_shell():
    runner = CliRunner()

    result = runner.invoke(root_plugin)
    assert result.exit_code == 0

    # test shell
    result = runner.invoke(root_plugin, ['dog', 'shell', '--help'])
    assert result.exit_code == 0
    assert """Shell""" in result.output




