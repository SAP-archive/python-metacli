import click
from metacli.decorators import loadPlugin, addBuiltin, permission, loadLogging
from metacli.util import get_logger


@loadLogging(logger_name="demotest")
@permission(root_permission=True)
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@addBuiltin(name="help")
@addBuiltin(name="shell")
@click.group(help='This tool\'s subcommands are loaded from a '
            'plugin folder dynamically.')
@click.pass_context
def core(ctx):
    """Test with apictl core"""
    if ctx.obj:
        return

    logger = get_logger("demotest")

    ctx.obj = {
        "logger": logger
    }

    ctx.obj["logger"].info("core entry root")
    ctx.obj["logger"].debug('This is a debug message')
    ctx.obj["logger"].info('This is an info message')
    ctx.obj["logger"].warning('This is a warning message')
    ctx.obj["logger"].error('This is an error message')
    ctx.obj["logger"].critical('This is a critical message')
    ctx.obj["logger"].info("core testing")


if __name__ == '__main__':
    core()

