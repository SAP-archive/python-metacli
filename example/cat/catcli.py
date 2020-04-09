import click
from metacli.decorators import loadPlugin, addBuiltin
from metacli.util import get_logger

@loadPlugin(json_file="plugin_commands.json",
            base_path=__file__)
@addBuiltin(name="schema")
@click.group()
@click.pass_context
def cat(ctx):
    """Welcome to cat's world"""
    logger = get_logger("cat")
    logger.debug("Entering cat Command Group")


@click.option("--name",
              help="input your name",
              default="")
@cat.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show cat's welcome"""
    pass


@click.option("--name",
              help="input your name",
              default="")
@cat.command("greeting")
@click.pass_context
def greeting(ctx, name):
    """Greeting from cat"""
    click.echo("Greeting from " + name)
