#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `metacli` package."""

import click
from click.testing import CliRunner


# Test Dynamic Plugin
def test_plugin_loader(root):
    runner = CliRunner()

    # root plugin test
    assert isinstance(root,click.Group)
    result = runner.invoke(root)
    assert result.exit_code == 0

    help_result = runner.invoke(root, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

    # load outer plugin
    result = runner.invoke(root)
    assert result.exit_code == 0

    help_result = runner.invoke(root, ['dog', '--help'])
    assert help_result.exit_code == 0
    assert "Welcome to dog\'s world" in help_result.output

    # load inner plugin
    help_result = runner.invoke(root, ['dog', 'cat', '--help'])
    assert help_result.exit_code == 0
    assert "Welcome to cat\'s world" in help_result.output


