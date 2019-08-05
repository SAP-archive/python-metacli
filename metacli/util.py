import json
import jsonschema
import click
import os
import logging

def check_valid_json(json_path):
    # the kind of json we expect in plugins_commands.json
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "click_root": {"type": "string"},
            "file_path": {"type": "string"},
            "package_path": {"type": "string"},
            "package_name": {"type": "string"}
        }
    }
    with open(json_path) as f:
        try:
            command_data = json.load(f)
            # validate given json is same as what is described in schema
            jsonschema.validate(command_data, schema)
        except jsonschema.exceptions.ValidationError as e:
            print("invalid json", e)
        except json.decoder.JSONDecodeError as e:
            print("text is not json", e)


def get_help_info(info, filename="help.json", display=False):
    """
    :param info: click.Group object where the root information from
    :param display: boolean, true means show structure in console
    :param filename: file name for help info
    :return: None
    """

    help_info = get_help_info_dfs(info)

    with open(filename, 'w') as fp:
        json.dump(help_info, fp, indent=2)

    if display:
        print(json.dumps(help_info, indent=2))

    if os.path.exists("help.json"):
        print("Generate help info in help.json")



def get_help_info_dfs(info):
    """
    :param info: click.Group object
    :return: dict of group info
    """
    group = info.__dict__

    group_info = {"name": group['name'],
                  "help": group["help"],
                  "hidden": group['hidden'],
                  "groups": [],
                  "commands": [],
                  "params": get_param_info(info)}

    for obj in group['commands'].values():
        if isinstance(obj, click.Group):
            group_info["groups"].append(get_help_info_dfs(obj))

        elif isinstance(obj, click.Command):
            command_info = obj.__dict__
            cmd = {"name" : command_info['name'],
                   "help" : command_info['help'],
                   "hidden": command_info['hidden'],
                   "params": get_param_info(obj)}
            group_info["commands"].append(cmd)

    return group_info


def get_param_info(info):
    """
    :param info: click.command or click.Object Object
    :return: dict of param info
    """
    params = info.__dict__['params']

    info_query_option = ['name', 'help', 'type', 'default', 'required', 'prompt']
    info_query_argument = ['name', 'type', 'default', 'required']
    params_info = []

    for param in params:
        if isinstance(param, click.Option):
            param_info = {key: str(param.__dict__[key]) for key in info_query_option}
            param_info['param_type'] = 'option'
        if isinstance(param, click.Argument):
            param_info = {key: str(param.__dict__[key]) for key in info_query_argument}
            param_info['param_type'] = 'argument'
        params_info.append(param_info)

    return params_info


# Get logger to write to log file.
# It has to be initialized every-time, since in a commandline application.
# the process is short-lived and new process is created for every invocation of a command.
def get_logger(logger_name):

    # default name and logger
    logger = logging.getLogger(str(logger_name))
    logger.setLevel(logging.DEBUG)
    file_name = str(logger_name) + ".log"
    fh = logging.FileHandler(file_name)
    formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(fh)


    return logger