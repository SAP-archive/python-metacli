import click
from metacli.decorators import loadPlugin, loadLogging, addBuiltin


@loadLogging(logger_name="testdemo")
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@addBuiltin(name="help")
@addBuiltin(name="shell")
@click.group(help='This tool\'s subcommands are loaded from a '
            'plugin folder dynamically.')
@click.pass_context
def core(ctx):
    """Test with apictl core"""
    pass



if __name__ == '__main__':
    core()

