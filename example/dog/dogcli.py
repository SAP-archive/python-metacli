import click
from metacli.decorators import loadPlugin, addBuiltin


@addBuiltin(name="shell")
@addBuiltin(name="schema")
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group()
@click.option('--version', default="1")
@click.option('--verbose', default="")
@click.pass_context
def dog(ctx, version, verbose):
    """Welcome to dog's world"""
    pass


if __name__ == '__main__':
    dog()
