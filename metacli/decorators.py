import functools
from .builtin_plugins import shell, schema
from .util import check_valid_json, get_logger
from .plugin import PluginLoader
import pathlib
import os
import json
import click
import sys
import stackprinter


def loadPlugin(func=None, *, json_file=None, base_path=None):
    """
    Decorate function to load plugins
    :param func: current click.Command / Group object
    :param json_file: plugin json in next level
    :param base_path: current plugin metacli.py path
    :return:
    """
    if func is None:
        return functools.partial(loadPlugin,
                                 json_file=json_file,
                                 base_path=base_path)

    @functools.wraps(func)
    def wrapper():
        base = pathlib.Path(base_path).resolve().parent
        plugin_json = str(base / json_file)

        # load plugins based on json
        if not os.path.exists(plugin_json):
            raise Exception("invalid path for" + plugin_json)
        else:
            with open(plugin_json) as f:
                check_valid_json(plugin_json)
                command_data = json.load(f)

            loader = PluginLoader(func, base)
            loader.load_plugin(command_data)

        return func

    return wrapper()


def addBuiltin(name=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            try:
                root = globals()[name]
                func.add_command(root)
            except KeyError:
                raise KeyError("Cannot find builtin plugin: " + name)
            return func
        return wrapper()
    return decorator


def loadLogging(func=None, *, logger_name="metacli"):
    """
    Decorate function to load logger
    :param func: current click.Command / Group object
    :param logger_name: name of logger
    :return:
    """
    if func is None:
        return functools.partial(loadLogging, logger_name=logger_name)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(logger_name)
        setattr(func, "logger", logger)
        try:
            return func.main(*args, **kwargs)
        except Exception:
            logger.exception("Exception occurred in CatchAllExceptions()")
            logger.error(stackprinter.format())
            file_location = logger.handlers[0].baseFilename
            click.echo("An error occurred during processing. Please check the log file at: " + file_location)
            sys.exit(1)

    return wrapper()
