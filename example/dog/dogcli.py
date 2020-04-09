import click
from metacli.decorators import loadPlugin, addBuiltin, loadLogging
from metacli.util import get_logger


@loadLogging(logger_name="dog")                 # create dog.log in current path to log activity
@addBuiltin(name="shell")                       # add built-in command shell
@addBuiltin(name="schema")                      # add built-in command schema
@loadPlugin(json_file="plugin_commands.json",   # plugin other command projects,
            base_path=__file__)                     # json_path: json file path relative to this file's path
@click.group()                                      # base_path: recommend using __file__ for now
@click.option('--version', default="1")
@click.option('--verbose', default="")
@click.pass_context
def dog(ctx, version, verbose):
    """Welcome to dog's world"""
    logger = get_logger("dog")                 # using dog.log to do logging
    logger.debug("Entering Dog Command Group")


if __name__ == '__main__':
    dog()
