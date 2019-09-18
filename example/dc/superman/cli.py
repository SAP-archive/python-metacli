import click
from metacli.decorators import loadPlugin, permission
from metacli.util import get_logger, set_context_obj

@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group()
@click.pass_context
def superman(ctx):
    """Test with superman"""

    # set own logger file
    logger = get_logger("superman")

    my_ctx_obj = {
        "logger": logger
    }

    set_context_obj(ctx, my_ctx_obj)

    ctx.obj['logger'].info("superman entry root")
    ctx.obj['logger'].info(click.get_os_args())


@permission(level="admin")
@click.option("--name",
              help="input your name",
              default="")

@superman.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show superman welcome"""
    click.echo("Hello " + name +  " superman ")
    ctx.obj['logger'].info("superman welcome")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("Hello " + name + " superman")


@permission(level="developer")
@click.option("--name",
              help="input your name",
              default="")
@superman.command("greeting")
@click.pass_context
def greeting(ctx, name):
    """show superman welcome"""
    click.echo("Greeting " + name +  " superman ")
    ctx.obj['logger'].info("superman welcome")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("Hello " + name + " superman")
