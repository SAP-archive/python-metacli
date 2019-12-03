import click
from metacli.decorators import loadPlugin

@loadPlugin(json_file="plugin_commands.json",
            base_path=__file__)
@click.group()
@click.pass_context
def ragdoll(ctx):
    """Test with superman"""
    pass


@click.option("--name",
              help="input your name",
              default="")
@ragdoll.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show ragdoll welcome"""
    pass


@click.option("--name",
              help="input your name",
              default="")
@ragdoll.command("running")
@click.pass_context
def running(ctx, name):
    """ragdoll can run"""
    pass
