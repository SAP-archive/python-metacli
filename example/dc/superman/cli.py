import click
from metacli.decorators import loadPlugin
from metacli.util import get_logger

@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group(invoke_without_command=True)
@click.pass_context
def superman(ctx):
    """Test with superman"""
    logger = get_logger("demotest")

    ctx.obj = {
        "logger": logger
    }

    ctx.obj['logger'].info("superman entry root")
    ctx.obj['logger'].info(click.get_os_args())


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



