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

def list_files(startpath):
    """
    Show files structure based on startpath in console
    :param startpath: path
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

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
