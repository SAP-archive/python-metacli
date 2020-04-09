import click
from metacli.util import get_logger


@click.group()
@click.pass_context
def bird(ctx):
    """Many different birds are here"""
    logger = get_logger("dog")
    logger.debug("Entering bird Command Group")


@click.option("--name",
              help="input your name",
              default="")
@bird.command("flying")
@click.pass_context
def flying(ctx, name):
    """bird can flying"""
    click.echo("Bird " + name + " can fly")


@bird.group("bluebird")
@click.pass_context
def bluebird(ctx):
    """bluebird is here"""
    click.echo("Bluebird is here")


@bird.command("dove")
@click.pass_context
def dove(ctx):
    """ Dove is here """
    click.echo("Dove is here")
