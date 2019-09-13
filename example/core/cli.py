import click
from metacli.decorators import loadPlugin, addBuiltin, permission, loadLogging
from metacli.util import get_logger, set_context_obj


# TESTING
# core --version 1 --verbose hi --pos 1.0 2.0 --message bye --message test --n 3 --item yi 2 -ttttt shell

@loadLogging(logger_name="demotest")
#@permission(root_permission=True)
@addBuiltin(name="shell")
@addBuiltin(name="schema")
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group(help='This tool\'s subcommands are loaded from a '
            'plugin folder dynamically.')
@click.option('--version', default = "1")
@click.option('--verbose', default = "")
@click.pass_context
def core(ctx, version, verbose) :
    """Test with apictl core"""
    if ctx.obj:
        return


    # set logger file
    logger = get_logger("demotest")

    my_ctx_obj = {
        "logger": logger
    }

    set_context_obj(ctx, my_ctx_obj)

    ctx.obj["logger"].info("core entry root")
    ctx.obj['logger'].info(click.get_os_args())

    ctx.obj["version"] = version
    ctx.obj["verbose"] = verbose
    click.echo("version: %s" % version)
    click.echo("verbose: %s" % verbose)


if __name__ == '__main__':
    core()

