#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `metacli` package."""

import click
from metacli.decorators import loadPlugin
from click.testing import CliRunner


@loadPlugin(json_file="./plugin_commands_test.json", base_path=__file__)
@click.group()
@click.pass_context
def root_plugin(ctx):
    """root plugin"""


# Test Dynamic Plugin
def test_plugin_loader():
    runner = CliRunner()

    # root plugin test
    assert isinstance(root_plugin, click.Group)
    result = runner.invoke(root_plugin)
    assert result.exit_code == 0

    help_result = runner.invoke(root_plugin, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

    # load outer plugin
    result = runner.invoke(root_plugin)
    assert result.exit_code == 0

    help_result = runner.invoke(root_plugin, ['dog', '--help'])
    assert help_result.exit_code == 0
    assert "Welcome to dog\'s world" in help_result.output

    # load inner plugin
    help_result = runner.invoke(root_plugin, ['dog', 'cat', '--help'])
    assert help_result.exit_code == 0
    assert "Welcome to cat\'s world" in help_result.output
