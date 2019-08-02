import click
from metacli.decorators import loadPlugin

@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group(invoke_without_command=True)
@click.pass_context
def superman(ctx):
    """Test with superman"""

@click.option("--name",
              help="input your name",
              default="")

@superman.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show superman welcome"""
    click.echo("Hello " + name +  " superman ")



