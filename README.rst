=======
MetaCLI
=======


.. image:: https://img.shields.io/pypi/v/metacli.svg
        :target: https://pypi.python.org/pypi/metacli

.. image:: https://img.shields.io/travis/tw4dl/metacli.svg
        :target: https://travis-ci.org/tw4dl/metacli

.. image:: https://readthedocs.org/projects/metacli/badge/?version=latest
        :target: https://metacli.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/tw4dl/metacli/shield.svg
     :target: https://pyup.io/repos/github/tw4dl/metacli/
     :alt: Updates



Python package to build metadata driven command line tools (CLI) with out-of-the-box REST Swagger/OpenAPI support


* Free software: Apache Software License 2.0
* Documentation: https://metacli.readthedocs.io.



Getting Start
-------------



>>> git clone https://github.wdf.sap.corp/Matrix/metacli.git

>>> cd metacli

>>> pip install .



Workflow
`````````
Create base plugin -> Configure json file
-> Add plugins
->

Run dependency management
-> run command line



Create plugins
...............

As a valid plugin, you need to include these three files:

| __init__.py
| cli.py : file that define your commands using Click library
| setup.py

To make the plugin as your base plugin, you need to include two more files:

| plugin_commands.json
| script_dependency_management.py (can be any name)

Configure plugin json file
..........................

Template for the json file:

| {
|   "modules" : [
|       {
|       }
|   ]
| }

| Each { } in modules is a plugin to be added to base plugin
| Valid plugin include these fields:
|   name : name of plugin shown in command line
|   click_root : the root command / group in your cli.py
|   package_path : relative path to plugin folder
|   package_name : <plugin_folder_name>.<cli.py>


Add Plugin
..........

Plugin
~~~~~~

To add a plugin:

| Clone the repo of the plugins
| Add to the <base_plugin>/plugin_commands.json as a plugin

Third-Party Plugin
~~~~~~~~~~~~~~~~~~

Support third-party plugins that are based on click. Add them in same way add plugins.

Builtin Plugin
~~~~~~~~~~~~~~

Support two builtin plugins shell and help:

| help: generate entire cmd structure json for all plugins and get help info
| shell: generate a prompt (just like shell )


To add builtin plugin to base plugin:

| Import addBuiltin to <base_plugin>.<cli.py> from metacli/decorators.py
| Add the plugin to <base_plugin>.<cli.py> using @addBuiltin(name = "<name_of_plugin>")

Run Dependency Management
.........................

| Create a script in the base plugin ( script_dependency_management.py ). We have a template in metacli/example/core
| Run script to generate requirements.txt: python script_dependency_management.py
| Check package conflicts
|   Check the console for messages about "Found a package of different versions in requirements.txt."
|   Go through the requirements.txt and pick the version that best fits your plugin
| Install the packages : pip install -r requirements.txt
|   Come across the error "Double Requirement given", try: cat dependencies.txt | xargs -n 1 pip install


Run Command Line
................

| Go into the base plugin folder
| Install the base plugin as common Click project: pip install --editable .
| To use it: <base_plugin> --help



Features
--------

* TODO

* Plugin json file
    * Support Relative and Absolute paths
        * Find plugins json file based on module
        * Relative paths to plugins based on parent module in cli.py
    * Check plugin json file is valid json

* Plugins
    * Support group level plugin based on json
        * Different plugins with same names are allowed in different levels
    * Support plugins functionality without need to change code
    * Support third party plugins based on click
    * Allow user to customize plugin's name
        * Different plugins with same names are allowed in the same level
        * Ability to choose and give meaningful names to the plugins

* Builtin Plugins
    *  Generate entire command structure and help info
* >>> <plugin_name> help --display # help.json will be generated and showed in console
    * Support shell prompt
* >>> <plugin_name> shell
    * Summarize all logs into user specified log file in base plugin

* Dependency Management
    * Gather all the required packages in plugins and pip install them
* >>> cd <base_plugin>/
* >>> python script_dependency_management.py # requirements.txt will be generated
* >>> pip install -r requirements.txt # install the required packages after resolve package conflicts in requirements.txt
* >>> cat requirements.txt | xargs -n 1 pip install # see "Double Requirement Error" when not change requirements.txt
    * Checks for dead loop for plugin
    * Checks for package version conflicts



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
