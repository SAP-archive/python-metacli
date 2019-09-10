import pathlib
import sys
import inspect
import importlib.util
import click
import os


class PluginLoader:

    def __init__(self, parent_plugin, base_path):
        self.parent_plugin = parent_plugin
        self.base_path = base_path

    def load_plugin(self, command_data):

        for module in command_data["modules"]:

            # get cli.py path
            package_name, package_path = module["package_name"], module['package_path']
            file_path = package_path + package_name.replace('.', '/') + '.py'
            file_path = self.parse_to_absolute_path(file_path)

            # get module absolute path to support relative import
            package_path = str((self.base_path / pathlib.Path(package_path)).resolve())
            sys.path.append(package_path)

            # load next plugin as dfs
            module_loaded = self.dynamic_load_from_path(package_name, file_path)
            # add subgroup into current group
            parent_command_name = module["click_root"]
            for name, obj in inspect.getmembers(module_loaded):
                if self.base_filter(obj, parent_command_name):
                    self.inject_attribute(obj, name=module['name'])
                    self.parent_plugin.add_command(obj)


    def inject_attribute(self, obj, **kwargs):
        """
        inject fields from json file
        :param obj: current click.Command / click.Group
        :param kwargs: injection arguments
        """
        for k, v in kwargs.items():
            if k in obj.__dict__:
                obj.__dict__[k] = v
            else:
                setattr(obj, k, v)

    def base_filter(self, obj, parent_command_name):
        """
        Base rules to filter subcommand / subgroup from all objects:
            1. is click.Group or click.Command
            2. the object is defined in current layer json
        :param obj: subcommadn / subgroup
        :param cur_command_name:
        :param parent_command_name:
        :return: boolean
        """

        # Filter out subcommands available for use if plugin run from terminal
        permission_commands  = self.filter_commands_by_permission_status(obj)
        if isinstance(obj, click.Command) and permission_commands and "shell" not in sys.argv:
            obj.commands = permission_commands

        return isinstance(obj, click.Command) \
               and obj.name == parent_command_name

    def filter_commands_by_permission_status(self, obj):
        permission_commands = {}
        functionlevel = "developer"

        userlevel = "developer"
        if os.path.exists(".temp.txt"):
            with open(".temp.txt", "r") as f:
                userlevel, timestamp = f.readline().rstrip().split("$")

        if isinstance(obj, click.Command):
            if "commands" in obj.__dict__:
                for cmd in obj.__dict__["commands"]:
                    cmd_obj = obj.__dict__["commands"][cmd]

                    # if there is permission, check if we can add the command for use
                    if "permission" in cmd_obj.__dict__:
                        functionlevel = cmd_obj.permission
                        if userlevel == "developer" and functionlevel == "admin":
                            pass
                        else:
                            permission_commands[cmd] = cmd_obj
                    else:

                        # if there is no permission, add command as developer, so both developers and admin can see
                        permission_commands[cmd] = cmd_obj

        return permission_commands

    def dynamic_load_from_path(self, module_name, path):
        spec = importlib.util.spec_from_file_location(module_name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def parse_to_absolute_path(self, next_path):
        """ current cli.py absolute path + relative next plugin path = absolute next plugin path"""
        return str((self.base_path / pathlib.Path(next_path)).resolve())
