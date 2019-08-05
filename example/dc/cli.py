import click
from metacli.decorators import loadPlugin


@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group()
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


# if __name__ == '__main__':
#     dc()


