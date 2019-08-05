import pathlib
import sys
import inspect
import importlib.util
import click


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
        return isinstance(obj, click.Command) \
               and obj.name == parent_command_name

    def dynamic_load_from_path(self, module_name, path):
        spec = importlib.util.spec_from_file_location(module_name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def parse_to_absolute_path(self, next_path):
        """ current cli.py absolute path + relative next plugin path = absolute next plugin path"""
        return str((self.base_path / pathlib.Path(next_path)).resolve())