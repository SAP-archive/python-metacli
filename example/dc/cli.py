import click
from metacli.decorators import loadPlugin, permission, addBuiltin
from metacli.util import get_logger, set_context_obj


@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@addBuiltin(name="schema")
@click.group()
@click.pass_context
def dc(ctx):
    """Test with DC superherors"""

    # use the parent logger demotest
    set_context_obj(ctx)

    ctx.obj['logger'].info("dc entry root")
    ctx.obj['logger'].info(click.get_os_args())


@permission(level = "developer")
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


