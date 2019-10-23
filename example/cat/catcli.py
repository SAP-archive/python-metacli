import click
from metacli.decorators import loadPlugin, addBuiltin
from metacli.util import get_logger, set_context_obj


@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@addBuiltin(name="schema")
@click.group()
@click.pass_context
def cat(ctx):
    """Welcome to cat's world"""

    # use the parent logger demotest
    # set_context_obj(ctx)
    #
    # ctx.obj['logger'].info("cat entry root")
    # ctx.obj['logger'].info(click.get_os_args())


@click.option("--name",
              help="input your name",
              default="")
@cat.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show cat's welcome"""
    click.echo("Hello " + name)

    ctx.obj['logger'].info("cat welcome")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("Hello " + name)


@click.option("--name",
              help="input your name",
              default="")
@cat.command("greeting")
@click.pass_context
def greeting(ctx, name):
    """Greeting from cat"""
    click.echo("Greeting from " + name)

    ctx.obj['logger'].info("cat greeting")
    ctx.obj['logger'].info(click.get_os_args())
    ctx.obj['logger'].info("Greeting from " + name)


# if __name__ == '__main__':
#     dc()


