import click
from metacli.decorators import loadPlugin, addBuiltin, loadLogging
from metacli.util import get_logger, set_context_obj


@loadLogging(logger_name="demotest")
@addBuiltin(name="shell")
@addBuiltin(name="schema")
@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group()
@click.option('--version', default = "1")
@click.option('--verbose', default = "")
@click.pass_context
def dog(ctx, version, verbose) :
    """Welcome to cat's world"""
    if ctx.obj:
        return


    # set logger file
    logger = get_logger("demotest")

    my_ctx_obj = {
        "logger": logger
    }

    set_context_obj(ctx, my_ctx_obj)

    ctx.obj["logger"].info("dog entry root")
    ctx.obj['logger'].info(click.get_os_args())

    ctx.obj["version"] = version
    ctx.obj["verbose"] = verbose


if __name__ == '__main__':
    dog()

