import click
from metacli.decorators import loadPlugin, addBuiltin, permission, loadLogging
from metacli.util import get_logger


@loadLogging(logger_name="demotest2")
@permission(root_permission=True)
@addBuiltin(name="shell")
@addBuiltin(name="schema")
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group(help='This tool\'s subcommands are loaded from a '
            'plugin folder dynamically.')
@click.pass_context
def core(ctx):
    """Test with apictl core"""
    if ctx.obj:
        return

    logger = get_logger("demotest2")


    ctx.obj = {
         "logger": logger,
    }

    ctx.obj["logger"].info("core entry root")
    ctx.obj['logger'].info(click.get_os_args())

if __name__ == '__main__':
    core()

