import os
import pathlib
import json
import distutils.core
import sys
import re
import jsonschema


class DependencyManagement:

    def __init__(self):
        ''' Dependency Management class '''
        print("Running DependencyManagement")

    def find_file(self, dir, file):
        '''
        Find the specific file in the directory
        :param dir: directory of the package
        :param file: name of file searching for
        :return: list of paths to that file
        '''

        file_list = []
        for fname in os.listdir(dir):
            if fname == file:
                file = os.path.join(dir, fname)
                file_list.append(file)

        return file_list

    def get_package_path(self, plugin_path, pkg_path, pkg_name):
        '''
        Get path to the plugin added to the current plugin
        :param plugin_path:
        :param pkg_path: path to go to package relative to parent plugin
        :param pkg_name: name of package and cli file
        :return: path to the package
        '''

        # Path to the plugin being added to the current module using package_path from module
        plugin_path_relative_parent = str((pathlib.Path(plugin_path).parent / pathlib.Path(pkg_path)).resolve())

        # Check the path to the plugin being added to current module points to the package or directory of package
        # If package path contains only "./", then plugin_path_relative_parents points to directory where package is,
        # so need to concatenate the package name from pkg_name to get actual path to module

        if re.match('^[./]+$', pkg_path):
            pkg_name_split = pkg_name.split(".")
            plugin_path_relative_parent = str((pathlib.Path(plugin_path_relative_parent) / pkg_name_split[0]).resolve())

        return plugin_path_relative_parent

    def create_packages_dictionary(self, list_packages):
        '''
        :param list_packages: list of all required packages found
        :return: dictionary of required package map to list of different versions of package found
        '''

        prefix_to_packages = {}
        for package in list_packages:

            # isolate the specific package name
            package_split = re.split("[> <]", package)
            package_prefix = package_split[0]

            if package_prefix not in prefix_to_packages:
                prefix_to_packages[package_prefix] = [package, ]
            else:
                prefix_to_packages[package_prefix].append(package)

        return prefix_to_packages

    def gather_packages_for_plugins_and_check_conflicts(self):
        '''
        Main function that gathers all the required packages for the plugins and checks for package conflicts
        '''

        self.gather_packages_for_plugins()

        self.check_package_conflicts()

    def detect_deadloop_for_plugins(self):
        ''' Function to detect deadloops'''
        path = input("Enter path to base plugin to start detecting deadloops: ")
        print("Path you enter,", path)
        if not os.path.exists(path):
            sys.exit("Path does not exist. Cannot gather the required packages")

        print("Detecting deadloops for plugins")
        packages_location = self.get_dependency_chain(path)

        if packages_location:
            print("No deadloops have been found")

    def gather_packages_for_plugins(self):
        ''' Function to gather all the required packages for plugins'''
        path = input("Enter path to base plugin to start gathering packages: ")
        print("Path you enter,", path)
        if not os.path.exists(path):
            sys.exit("Path does not exist. Cannot gather the required packages")

        print("Gathering all the required packages")

        # Get the location of the setup.py where we can get
        packages_location = self.get_dependency_chain(path)

        required_packages = self.get_packages_from_setup(packages_location)

        print("Saving required packages in requirements.txt")
        # Save the required dependencies in a file requirements.txt

        file_path = path + "/requirements.txt"

        with open(file_path, "w") as f:
            for package in required_packages:
                f.write(package + "\n")

        f.close()

        print("Finish getting all required packages \n")

    def check_package_conflicts(self):
        ''' Function to check package conflicts'''
        print("Checking for package of different versions conflict in requirements.txt")
        foundConflict = self.check_packages_different_version()

        if not foundConflict:
            print("No conflicts found. Safely run the base plugin")

    def get_dependency_chain(self, module_path):
        '''
        Get the setup.py for the plugins required in plugins
        :param module_path: path to main plugins that is base plugin, other plugins add to base plugin
        :return: all_setups: list of paths to setup.py
        '''

        all_plugins = []
        plugins_get_dependencies = []
        all_setups = []

        # Get the dependencies for base plugin

        # Find path to the setup.py
        all_setups = self.check_only_one_setup_exists(module_path, all_setups)

        # Find path to the plugin_commands.json
        plugins_get_dependencies = self.check_and_get_valid_plugin(module_path, plugins_get_dependencies)

        # Get the dependencies from the plugins based on plugin_commands.json and setup.py
        while plugins_get_dependencies:
            plugin_path = plugins_get_dependencies.pop(0)
            all_plugins.append(plugin_path)

            # Find the plugin_commands.json and setup.py of plugins
            new_setup, new_plugins = self.get_plugin_dependencies(plugin_path)

            all_setups = list(set(all_setups + new_setup))

            # Ensure only search through plugins not seen before
            self.check_deadloop(new_plugins, all_plugins, plugin_path)
            plugins_add, all_plugins = self.check_seen_plugins(new_plugins, all_plugins)
            plugins_get_dependencies = list(set(plugins_get_dependencies + plugins_add))

        return all_setups

    def get_packages_from_setup(self, all_setups):
        '''
        Gathers the packages from the setup.py
        :param all_setups: list of paths to the setup.py
        :return: list of all packages found
        '''
        # Get all required dependencies from install_requires in setup.py
        current_directory = os.getcwd()

        all_packages = []
        for setup_file in all_setups:
            parent = str(pathlib.Path(setup_file).parent.resolve())
            os.chdir(parent)
            setup = distutils.core.run_setup(setup_file)
            packages = setup.install_requires
            all_packages = list(set(all_packages + packages))

        all_packages.sort()
        os.chdir(current_directory)

        return all_packages

    def check_packages_different_version(self):
        '''
        Checks for packages of different versions in requirements.txt
        '''

        all_packages = []
        foundConflict = False

        # Get path to requirements.txt
        path = input("Enter path to base plugin to check the requirements.txt: ")
        print("Path you enter,", path)
        if not os.path.exists(path):
            sys.exit("Path does not exist. Cannot check requirements.txt")

        file_path = path + "/requirements.txt"

        # Get packages from requirements.txt
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    all_packages.append(line.rstrip())
        except IOError:
            sys.exit("Could not read file: requirements.txt \nPlease create file first in base plugin")

        # Check if requirements.txt includes packages of different versions before do pip install
        # Create dictionary of required packages that map package to list of different versions found
        dictionary_packages = self.create_packages_dictionary(all_packages)

        # List out packages that have different versions for users to look over
        for package_prefix, list_packages in dictionary_packages.items():
            if len(list_packages) > 1:
                print("Found a package of different versions in requirements.txt for: " + package_prefix)
                foundConflict = True
                for pkg in list_packages:
                    print(pkg)
                print("Please check the requirements.txt and pick one you want to use \n")

        return foundConflict

    def check_deadloop(self, new_plugins, allocated_plugins, curr_path):
        '''
        Check for deadloop for plugins and stop program if found
        :param new_plugins: list of plugins that will be added to current plugin
        :param allocated_plugins: existing list of all plugins that have been added to base plugin
        :param curr_path: path to current plugin which gathering packages for
        '''

        for plugin in new_plugins:
            if plugin in allocated_plugins:
                sys.exit("Dead loop detected between new plugin " + plugin + " and existing plugin " + curr_path)

    def check_seen_plugins(self, new_plugins, allocated_plugins):
        '''
        Check if come across plugin_commands.json before
        :param new_plugins: new plugin_commands.json found
        :param allocated_plugins: existing list of plugin_commands.json
        :return: plugin_commands.json have not come across before
        '''
        plugins_to_add = []
        for plugin in new_plugins:
            if plugin not in allocated_plugins:
                plugins_to_add.append(plugin)

        return plugins_to_add, allocated_plugins

    def get_plugin_dependencies(self, path_plugins):
        '''
        Get the setup.py and plugin_commands.json in plugins
        :param path_plugins: path to plugin directory
        :return: setup.py and plugin_commands.json of plugin
        '''
        setup_list = []
        plugins_list = []

        with open(path_plugins) as f:
            command_data = json.load(f)

        for module in command_data["modules"]:
            # Get the path to where the package is located
            package_name = module["package_name"]
            package_path = module['package_path']

            # Get the location of the package
            package_directory = self.get_package_path(path_plugins, package_path, package_name)

            # Find the location of the setup.py in package
            setup_list = self.check_only_one_setup_exists(package_directory, setup_list)

            # Find the location of the plugin_commands.json starting in package
            plugins_list = self.check_and_get_valid_plugin(package_directory, plugins_list)

        return setup_list, plugins_list

    def check_only_one_setup_exists(self, package_directory, list_setups):
        '''
        Ensures there can only be one setup.py for the plugin to be valid
        :param package_directory: path to the plugin directory
        :param list_setups: existing list of all setups found
        :return: updated list of all setups including newest one found
        '''

        # Get list of paths to all setup.py that exists in the plugin
        setup_lists = self.find_file(package_directory, "setup.py")
        if len(setup_lists) < 1:
            sys.exit("Cannot find setup.py in " + package_directory + ". Please create a setup.py and try again")
        elif len(setup_lists) > 1:
            sys.exit("Found multiple setup.py in " + package_directory + ". There can only be one")
        else:
            setup_location = setup_lists[0]
            list_setups.append(setup_location)

        return list_setups

    def check_and_get_valid_plugin(self, package_directory, list_jsons):
        '''
        Ensures there can only be one or zero plugin_commands.json for the plugin to be valid
        :param package_directory: path to the plugin directory
        :param list_jsons: existing list of all plugin jsons found
        :return: updated list of all plugin jsons including newest one found
        '''

        # Get list of paths to all plugin_commands.json that exists in the plugin
        plugin_lists = self.find_file(package_directory, "plugin_commands.json")
        if len(plugin_lists) < 1:
            pass
        elif len(plugin_lists) > 1:
            sys.exit("Found multiple plugin_commands.py in " + package_directory + ". There can only be one")

        else:
            plugin_location = plugin_lists[0]
            self.check_valid_json(plugin_location)
            list_jsons.append(plugin_location)

        return list_jsons

    def check_valid_json(self, json_path):
        '''
        Ensures the plugin_commands.json is valid format
        :param json_path: path to the plugin_commands.json
        '''
        # the kind of json we expect in plugins_commands.json
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "click_root": {"type": "string"},
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

