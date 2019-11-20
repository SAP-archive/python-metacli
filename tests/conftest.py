from metacli.decorators import loadPlugin
import click
import pytest


@pytest.fixture(scope="session")
def root():

    @loadPlugin(json_file="./plugin_commands_test.json", base_path=__file__)
    @click.group()
    @click.pass_context
    def root_plugin(ctx):
        """root plugin"""
        pass

    return root_plugin
