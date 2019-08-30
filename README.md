# MetaCLI

[![pypi](https://img.shields.io/pypi/v/metacli.svg)](https://pypi.python.org/pypi/metacli)
[![build](https://img.shields.io/travis/tw4dl/metacli.svg)](https://travis-ci.org/tw4dl/metacli)
[![docs](https://readthedocs.org/projects/metacli/badge/?version=latest)](https://metacli.readthedocs.io/en/latest/?badge=latest)
[![pyup](https://pyup.io/repos/github/tw4dl/metacli/shield.svg)](https://pyup.io/repos/github/tw4dl/metacli/)



Python package to build metadata driven command line tools (CLI) with out-of-the-box REST Swagger/OpenAPI support


+ Free software: Apache Software License 2.0
+ Documentation: https://metacli.readthedocs.io.



## Getting Start


```
git clone https://github.wdf.sap.corp/Matrix/metacli.git

cd metacli

pip install .

```

### Workflow

Create base plugin -> Configure json file -> Add plugins
-> Run dependency management -> Run command line



### Create plugins

As a valid plugin, you need to include these three files:
+  \_\_init\_\_.py
+ cli.py : file that define your commands using Click library
+ setup.py

To make the plugin as your base plugin, you need to include one more file:

+ plugin_commands.json

### Configure plugin json file


Schema for the valid plugin json file:
```
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

```

Each { } in modules is a plugin to be added


### Add Plugin

To add existing plugins to the base plugin:

+ Add the decorator, loadPlugin, to the base plugin in the cli.py based on plugin json file

```
from metacli.decorators import loadPlugin

@loadPlugin(json_file="./plugin_commands.json",
            base_path=__file__)
@click.group()
def base_plugin():
    pass
    
```
Parameters: 
+ json_file: relative path to the plugin json file
+ base_path: current cli file path

#### Third-Party Plugin

Support third-party plugins that are based on click. Add them in same way add plugins.

#### Builtin Plugin
Support two builtin plugins shell and schema:

+ schema: generate entire cmd structure json for all plugins and get help info
+ shell: generate a prompt (just like shell )



To add builtin plugins to base plugin cli.py:

```
from metacli.decorators import addBuiltin

@addBuiltin(name="schema")
@addBuiltin(name="shell")
@click.group()
def base_plugin():
    pass
```

### Run Dependency Management

+ Run dependency management in the console as a command line to generate requirements.txt: 
    ```
    metacli dependency_management
    ```
    + Note: enter the absolute path to the base plugin folder 
+ Check package conflicts
    + Check the console for messages about "Found a package of different versions in requirements.txt."
    + Go through the requirements.txt and pick the version that best fits your plugin
+ Install the packages : 
    ``` 
    pip install -r requirements.txt
    ```
 + If you choose to not resolve the package conflicts and want to install the first appeared version of the conflict packages, try: 
    ``` 
    cat dependencies.txt | xargs -n 1 pip install
    ```


### Run Command Line

+ Go into the base plugin folder
+ Install the base plugin as common [Click project](https://palletsprojects.com/p/click/): 
    
    ```
    pip install --editable .
    ```
+ To use it:
    ```
    <base_plugin> --help
    ```


## Features
+ **Plugin json file**
    + Support Relative and Absolute paths
        + Find plugins json file based on module
        + Relative paths to plugins based on parent module
    + Check plugin json file is valid json

+ **Plugins**
    + Support group level plugin based on json
        + Different plugins with same names are allowed in different levels
    + Support plugins functionality without need to change code
    + Support third party plugins based on click
    + Allow user to customize plugin's name
        + Different plugins with same names are allowed in the same level
        + Ability to choose and give meaningful names to the plugins

+ **Builtin Plugins**
    +  Generate entire command structure and help info
        ```
         <plugin_name> schema --display # help.json will be generated and showed in console
         ```
    + Support shell prompt
        ```
         <plugin_name> shell
         ```
        + Logs all the commands run in the shell in generated file shell_history
        + Saves all parameter values in hidden file parameters_history
        + Loads the latest saved parameter for use in the shell
        + Built in Commands:
            ```
             <plugin_name> > :q
            ```
            + Use *:q* to quit the shell
            ```
            <plugin_name> > --help
            ```
            + Use *--help* to show all the available commmands that can be used
            ```
            <plugin_name> > --history
            ```
            + Use *--history* to show all saved parameter values
+ **Dynamic Loading**
    + Absolute path import between different plugins based on json file
    + Relative path import in one plugin project based on cli file

+ **Dependency Management**
    + Gather all the required packages in plugins and pip install them
    + Checks for dead loop for all plugins
    + Checks for package version conflicts

+ **Logging**
    + Catch all exceptions into user specified log file in base plugin using decorator *loadLogging*
    + Summarize all logs into user specified log file in base plugin
        + Use *get_logger* to specify log file and get the logger
        + Save logger as part of context for base plugin using *set_context_obj* 
        ```
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
        ```
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
                    ```
                        set_context_obj(ctx, my_ctx_obj)
                    ```
             + To use the same log file, then directly call 
                ```
                    set_context_obj(ctx)
                ```
+ **Permission Control**
    + Add permissions of *admin* and *developer* to Click groups and commands in the cli.py. Default is *developer*.
    ```
        from metacli.decorators import permission
        
        @permission(level = "developer", root_permission=True)
        @click.group()
        def base_plugin():
            pass
    ```
    + Add login / logout features in Click root of base plugin (when we set root_permission = True). 
    + Keep login status for 60 seconds after each login
    + TODO: Verification
    
## Example
We provide an example to help you construct CLI tools.

In example folder, we have four independent projects, the file structure is:

| -- core\
| -- dc\
|&nbsp; &nbsp; &nbsp; &nbsp; |-- superman\
| -- marvel

All projects satisfy the basic plugin schema we described above, which means you can run them independently.
We want to construct the plugin tool structure as:

-- core \
&nbsp; &nbsp; &nbsp; &nbsp;    |-- dc \
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |-- superman\
&nbsp; &nbsp; &nbsp; &nbsp;    | -- marvel
        
        
Now we start to do this step by step.

1. Configure json file to construct structure

    In this structure, we need two json files, one is under *core* which will add the *marvel* and *dc*, another is in *dc* which will add *superman*.

    (in our example plugin_commands.json file, we also add mySQLcli and SQLlitecli to show how to add third-party plugins, if you don't need them, feel free to delete them and try our example)

2. Add plugin loader

    In *core* and *dc*, we need to load plugin from json file. So we add the loader on the parent click object through decorator. Two arguments, json_path and base_path, are required here. We need to add loaders in *core.cli.py* and *dc.cli.py*.

3. Collect and install all required packages

    Right now, core is our root. So, we need to do dependency management from core. Firstly, run dependency management in the console as a command line to collect all packages
    ```
    metacli dependency_management
    ```
    The input is current plugin project's absolute path. For example, right now we are in core, so the path will be  ```~/metacli/example/core```. Also, you need to input the location where you want to get your requirements.txt. For example, here we also use ```~/metacli/example/core```. After deleting conflicts in requirements.txt, you can use pip to install all required packages in one command
    ```
    pip install -r requirements.txt
    ```

4. Install and run CLI tools:

    Now, you can install CLI tools as command click projects.
    ```
    cd core/
    pip install --editable .
    core --help
    ```

5. Optional: Builtin Plugins:

    We have provided some built-in plugins(shell, help). If you want to add these plugins to any command or group. just use decorator to add them. The argument name should be "schema" or "shell" indicating help plugin or shell plugin

6. Optional: Permission:
    
    We can add permission control in our system. After set *core* as permission root, there will be two commands: login / logout under *core*. Also, we wrote some permission controlled commands under *dc*. If you want to run command as admin, please login first. You can choose logout manually or the login status will be expired in 1 min. 

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.



