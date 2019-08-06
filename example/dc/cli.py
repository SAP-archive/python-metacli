import click
from metacli.decorators import loadPlugin, permission


@permission(level = "developer")
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group(hidden=True)
@click.pass_context
def dc(ctx):
    """Test with DC superherors"""
    pass


@click.option("--name",
              help="input your name",
              default="")
@dc.command("welcome")
@click.pass_context
def welcome(ctx, name):
    """show DC welcome"""
    click.echo("Hello " + name +  " DC World ")


@permission(level = "admin")
@click.option("--name",
              help="input your name",
              default="")
@dc.command("greeting")
@click.pass_context
def greeting(ctx, name):
    """Greeting DC welcome"""
    click.echo("Greeting " + name +  " DC World ")


# if __name__ == '__main__':
#     dc()


