import click
from metacli.decorators import loadPlugin
from metacli.util import get_logger, set_context_obj

@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group()
@click.pass_context
def ragdoll(ctx):
    """Test with superman"""

    # set own logger file
    logger = get_logger("ragdoll")

    my_ctx_obj = {
        "logger": logger
    }

    set_context_obj(ctx, my_ctx_obj)

    ctx.obj['logger'].info("ragdoll entry root")
    ctx.obj['logger'].info(click.get_os_args())


@click.option("--name",
              help="input your name",
              default="")
@ragdoll.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show ragdoll welcome"""
    click.echo("Hello " + name)
    ctx.obj['logger'].info("ragdoll welcome")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("Hello " + name)


@click.option("--name",
              help="input your name",
              default="")
@ragdoll.command("running")
@click.pass_context
def running(ctx, name):
    """ragdoll can run"""
    click.echo("ragdoll " + name + " is running")
    ctx.obj['logger'].info("ragdoll running")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("ragdoll " + name + " is running")
