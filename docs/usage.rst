.. highlight:: shell

=====
Usage
=====

Add Plugin
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
                "package_path" : <relative path to plugin folder>,
                "package_name" : <plugin_folder_name>.<cli.py>
               }
           ]
         }

    Please jump to our example to examples if you still have questions here.

- Add the decorator, loadPlugin, to the base plugin in the cli.py based on plugin json file

    .. code-block:: python

        from metacli.decorators import loadPlugin

        @loadPlugin(json_file="./plugin_commands.json",
                    base_path=__file__)
        @click.group()
        def base_plugin():
            pass



    - Parameters:
        + json_file: relative path to the plugin json file
        + base_path: current cli file path

- Supported Plugin

    Now we can support command line project based on Click.
    Here are some open-sourced Click project on Github:
        - mycli : https://www.mycli.net/
        - pgcli : https://www.pgcli.com/


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


Run Command Line
--------------
The running for this plugined project is same as Click project, make sure the relative plugin path is correct when you
run the base plugin.

+ Go into the base plugin folder
+ Install the base plugin as common [Click project](https://palletsprojects.com/p/click/):

    .. code-block:: console

        pip install --editable .

+ To use it:

    .. code-block:: console

        <base_plugin> --help

Built-in Plugin
--------------

MetaCLI support some built-in plugin. You can add these plugins to any command layer within 1 line code.


To add builtin plugins:

.. code-block:: console

    from metacli.decorators import addBuiltin

    @addBuiltin(name="schema")
    @addBuiltin(name="shell")
    @click.group()
    def base_plugin():
        pass


shell prompt
>>>>>>>>>

MetaCLI can help you use prompt to run all commands, also can help you save and retrieve parameters in different command layers.

To use it, add "shell" in your code, and you can run this command in your console:

.. code-block:: console

    <plugin_name> shell


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

When a lot of plugins are added into base, it maybe hard for user to know the entire structure for the command lines,
so we provide the schema describing plugin.

To use it, add the "schema" plugin into code, and run this command in
console :

.. code-block:: console

    <plugin_name> schema --display

Tips:
    + --display is an optional argument, is this one is added, the structure will be shown in console
    + "schema.json" will be generated in current folder.This file describe the command, argument and etc.


Templates
--------------
We provide templates to help user create their own command line project easily.

Simple Templates
>>>>>>>>>

To create an simple command line project, run this command in terminal:

.. code-block:: console

    $ metacli create_project

We need to input the path and the name for this new project in terminal. Then we can see this new project.
In this new project, we have 6 files.

- project core files
    - **setup.py**: the file which can install the project to system

    - **<name>cli.py**: the file which contains all command

    - **__init__.py**: indicate this project as Python package, you can define your version number here

- project plugin files:
    - **plugin_commands.json**: this is a file where you can plugin other command line projects

- template files:\
    - **schema.json**: this is a template file written in JSON, you can define your command structure and name as the examples in this file

    - **schema.yaml**: this file is same as schema.json, the only difference is it is written in yaml

This project can be run directly as a hello world example, just run this command in your terminal when you are in this project directory:

.. code-block:: console

    $ pip install --editable .

    $ <project name> hello-world

This is same as how to run a command based on Click Library, and you can get a hello world command when you run you command

.. code-block:: console

    $ hello world <project name>

Complex Templates
>>>>>>>>>
In the above session, we mentioned we have 2 template schema files, we can write these files and use our metalcli to generate a more complex
project easily.

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

We have provided an example in our template file, you can try this example directly:

.. code-block:: console

    $ metacli create_project --fromjson '<path for template JSON file>'

Then, we can get a new project with the command and argument defined in our json file.

The YAML file is similar, the only difference here is:

.. code-block:: console

    $ metacli create_project --fromyaml '<path for template YAML file>'

In this example, after you install the new project and run our example:

.. code-block:: console

    $ <project name>  example_command --example_argument <test parameter>

    $ this is group example_group
    $ parameters:
    $ this is command example_command
    $ parameters: <test parameter>


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





