.. highlight:: shell

=====
Features
=====

Command Plugin
--------------

To add existing plugins to the base plugin:

- configure plugin json file

    Each { } in modules is a plugin to be added. Schema for the valid plugin json file:

    .. code-block:: console

         {
           "modules" : [
               {
                "name" : <name of plugin shown in command line>,
                "click_root" : <the root command / group in cli.py>,
                "package_path" : <relative path to plugin folder based on cli file>,
                "package_name" : <plugin_folder_name>.<cli.py>
               }
           ]
         }

    Please check the example on getting start for real usage.

- Add the decorator, loadPlugin, to the base plugin in the cli.py based on plugin json file

    .. code-block:: python

        from metacli.decorators import loadPlugin

        @loadPlugin(json_file="plugin_commands.json",
                    base_path=__file__)
        @click.group()
        def base_plugin():
            pass



    - Parameters:
        + json_file: the plugin JSON file's name
        + base_path: current cli file path

- Supported Plugin

    Now we can support command line project based on Click.
    Here are some open-sourced Click project on Github:
        - mycli : https://www.mycli.net/
        - pgcli : https://www.pgcli.com/
- example: :ref:`example-doc`


Dependency Management
--------------
Once some plugins are added into base plugin, the package dependency or conflicts need to be solved. So, before starting to run
this project, the dependency management need to be used firstly.

+ Run dependency management in the console as a command line to generate requirements.txt:
    .. code-block:: console

        metacli dependency_management

    + Note: enter the absolute path to the base plugin folder

+ Check package conflicts
    + Check the console for messages about "Found a package of different versions in requirements.txt."
    + Go through the requirements.txt and pick the version that best fits your plugin

+ Install the packages :

    .. code-block:: console

        pip install -r requirements.txt

+ If you choose to not resolve the package conflicts and want to install the first appeared version of the conflict packages, try:

    .. code-block:: console

        cat requirements.txt | xargs -n 1 pip install

Built-in Plugin
--------------

MetaCLI support some built-in plugin. These commands can be added using decorator:

.. code-block:: console

    from metacli.decorators import addBuiltin

    @addBuiltin(name="schema")
    @addBuiltin(name="shell")
    @click.group()
    def base_plugin():
        pass


shell prompt
>>>>>>>>>

MetaCLI shell support running all commands in interactive prompt, also support save and retrieve parameters in different command layers.

To use it, use "shell" as command:

.. code-block:: console

    <plugin_name> shell

Features:

+ Logs all the commands run in the shell in generated file shell_history

+ Saves all parameter values in hidden file and allow other commands to read the latest saved parameters in shell

+ Built in Commands:
    .. code-block:: console

        <plugin_name> > :q

    + Use *:q* or *:quit* to quit the shell
    .. code-block:: console

        <plugin_name> > :help

    + Use *:help* or *:h* to show all the available commmands and saved options for a group
    .. code-block:: console

        <plugin_name> > :shell_history

    + Option “—debug”: to show all saved parentheses for all group level sessions.

    + Use *:shell_history* or *:sh* to show all saved parameter values for current group level session and previous group level sessions
    .. code-block:: console
        <plugin_name> > :set <parameter_name_without_dashes>=<parameter_value>

    + Use *:set* or *:s* to set a value for a specify parameter




schema description
>>>>>>>>>

When a lot of plugins are added into base, it maybe hard for user to know the entire structure for this command.
so Metacli provide the schema describing plugin.

To use it, add the "schema" plugin into code, and run thE command:

.. code-block:: console

    <plugin_name> schema --display

Tips:
    + --display is an optional argument, is this one is added, the structure will be shown in console
    + "schema.json" will be generated in current folder.This file describe the commands, arguments and etcs.

.. _new-project-generator:

Project Generator
--------------
MetaCLI can help to generate a new project easily.

Simple Project
>>>>>>>>>

To create an simple command line project, run this command in terminal:

.. code-block:: console

    $ metacli create_project # (optional) --inlcude_template True

To use default path and name (current path and helloworld), just press Enter in prompt. Also you can input the path and the name for this new project. Then a new project is generated.
In this new project, here is the file structure.

- project core files
    - **setup.py**: the file which can install the project to system

    - **<name>cli.py**: the file which contains all command

    - **__init__.py**: indicate this project as Python package, the version can be defined here

- project plugin files:
    - **plugin_commands.json**: plugin configuration file

- template files (only appear if using --include_template True):\
    - **schema.json**: this is a template schema file written in JSON.

    - **schema.yaml**: this file is same as schema.json, the only difference is it is written in yaml

This project can be run directly as a hello world command:

.. code-block:: console

    # in new project's folder
    $ pip install --editable .

    $ helloworld --help

Complex Project from templates
>>>>>>>>>
In the above session, we have 2 template schema files, MetalCLI can generate a complex project based on schema file easily.

Here we take the JSON format as an example, the YAML file is similar

Three different data structures in click are supported now in our generator: Group, Command and Option

We list the required fields for each structure:

- group:
    - name: String, define the name for this group
    - help: String, help information for this group
    - hidden: Boolean String ["True", "False"], whether this group is hidden or not
    - groups: List, subgroups under this group
    - commands: List, commands under this group
    - params: List, parameters for this group
- command:
    - name: String, define the name for this command
    - help: String, help information for this command
    - hidden: Boolean String ["True", "False"], whether this command is hidden or not
    - params: List, parameters for this command
- parameters:
    - name: String, parameter name
    - help: String, help information for this parameter
    - type: String ["BOOL", "STRING"], define the data type for this parameter
    - default: String: default value for this argument, must satisfy the data type you defined
    - required: Boolean String ["True", "False"], whether this is a required parameter or not
    - prompt: Boolean String ["True", "False"], define the input method for this parameter
    - param_type: "option" (only support option right now)

The sample template is provided when the argument --include_template is true. A new project can be generated based on this sample schema directly:

.. code-block:: console

    $ metacli create_project --fromjson '<path for template JSON file>'

Then, a new project is generated.

The YAML file is similar, the only difference here is:

.. code-block:: console

    $ metacli create_project --fromyaml '<path for template YAML file>'

To use this sample project:

.. code-block:: console

    $ <project name>  example_command --example_argument <test parameter>

    $ this is group example_group
    $ parameters:
    $ this is command example_command
    $ parameters: <test parameter>

.. _logging-doc:

Logging
--------------


MetaCLI support a simple logging system, this feature can be used as following:

+ Catch all exceptions into user specified log file in base plugin using decorator *loadLogging*

+ Summarize all logs into user specified log file in base plugin
    + Use *get_logger* to specify log file and get the logger
    + Save logger as part of context for base plugin using *set_context_obj*
    .. code-block:: python

        from metacli.decorators import loadLogging
        from metacli.util import get_logger, set_context_obj

        @loadLogging(logger_name=<specified_log_file>)
        @click.group()
        def base_plugin(ctx):
            if ctx.obj:
                return

            logger = get_logger(<specified_log_file>)

            my_ctx_obj = {
                "logger": logger
            }

            set_context_obj(ctx, my_ctx_obj)


 + *set_context_obj* sets the context object that allows user to add atributes to context
    + Parameters:
        + ctx : context for the plugin
        + my_ctx_obj : *optional* user defined dictionary of attributes for context
    + Allow logging with different contexts for plugins at different levels
        + Child plugins can add attributes to the context of parent plugin
            + Create *my_ctx_obj* to specify new attributes for context
            + Call *set_context_obj* with both parameters *ctx* and *my_ctx_obj*
    + Can specify different log files for plugins at different levels or use same logger
        + To use different log file for a plugin:
            + Call *get_logger* to get different log file and logger
            + Create *my_ctx_obj* with new logger
            + Call
            .. code-block:: python

                set_context_obj(ctx, my_ctx_obj)

        + To use the same log file, then directly call
        .. code-block:: python

            set_context_obj(ctx)





