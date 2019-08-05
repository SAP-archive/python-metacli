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

To make the plugin as your base plugin, you need to include two more files:

+ plugin_commands.json
+ script_dependency_management.py (can be any name)

### Configure plugin json file


Schema for the valid plugin json file:
```
 {
   "modules" : [
       {
        "name" : "name of plugin shown in command line",
        "click_root" : "the root command / group in cli.py",
        "package_path" : "relative path to plugin folder",
        "package_name" : "<plugin_folder_name>.<cli.py>"
       }
   ]
 }

```

Each { } in modules is a plugin to be added


### Add Plugin

To add an existing plugins to the base plugin:

+ Add the decorator, loadPlugin,  to the base plugin based on plugin json file in the cli.py

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
Support two builtin plugins shell and help:

+ help: generate entire cmd structure json for all plugins and get help info
+ shell: generate a prompt (just like shell )



To add builtin plugin to base plugin cli.py:

```
from metacli.decorators import addBuiltin

@addBuiltin(name="help")
@addBuiltin(name="shell")
@click.group()
def base_plugin():
    pass
```

### Run Dependency Management

+ Create a script in the base plugin ( script_dependency_management.py ). We have a template in metacli/example/core
+ Run script to generate requirements.txt: 
    ```
    python script_dependency_management.py
    ```
+ Check package conflicts
    + Check the console for messages about "Found a package of different versions in requirements.txt."
    + Go through the requirements.txt and pick the version that best fits your plugin
+ Install the packages : 
    ``` 
    pip install -r requirements.txt
    ```
    + Come across the error "Double Requirement given", try: 
        ``` 
        cat dependencies.txt | xargs -n 1 pip install
        ```


### Run Command Line

+ Go into the base plugin folder
+ Install the base plugin as common Click project: 
    
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
         <plugin_name> help --display # help.json will be generated and showed in console
         ```
    + Support shell prompt
        ```
         <plugin_name> shell
         ```
    + Summarize all logs into user specified log file in base plugin
        ```
        from metacli.decorators import loadLogging
        
        @loadLogging(logger_name="<specified_log_file>")
        @click.group()
        def base_plugin():
            pass
        ```

+ **Dependency Management**
    + Gather all the required packages in plugins and pip install them
    + Checks for dead loop for all plugins
    + Checks for package version conflicts



## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

_Cookiecutter: https://github.com/audreyr/cookiecutter

_`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

