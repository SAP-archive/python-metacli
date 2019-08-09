import click
from metacli.decorators import loadPlugin, permission
from metacli.util import get_logger


@permission(level = "developer")
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group(hidden=True)
@click.pass_context
def dc(ctx):

    logger = get_logger("demotest")

    ctx.obj = {
        "logger": logger
    }

    """Test with DC superherors"""
    ctx.obj['logger'].info("dc entry root")
    ctx.obj['logger'].info(click.get_os_args())



@click.option("--name",
              help="input your name",
              default="")
@dc.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show DC welcome"""
    click.echo("Hello " + name +  " DC World ")
    ctx.obj['logger'].info("dc welcome")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("Hello " + name + " DC World")


@permission(level = "admin")
@click.option("--name",
              help="input your name",
              default="")
@dc.command("greeting")
@click.pass_context
def greeting(ctx, name):
    """Greeting DC welcome"""
    click.echo("Greeting " + name +  " DC World ")
    ctx.obj['logger'].info("dc greeting")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("Greeting " + name + " DC World")


# if __name__ == '__main__':
#     dc()


