.. highlight:: shell

============
Getting Start
============
We provide an example to help you getting start.

In example folder, we have 5 independent projects, the file structure is:

| -- bird\
| -- cat\
|   |-- ragdoll\
| -- dog
| -- testing_shell

All projects are the simplest command line project based on Click, which means you can run them independently.

However, we want to construct the plugin tool structure as:

-- cog \
  |-- cat \
    |--ragdoll\
  |-- bird\
    |-- testing_shell


Now we start to do this step by step.

1. Configure json file to construct structure
--------------

Firstly, we want to plug *cat* into *dog*. So, the example/bird/plugin_commands.json needs to be modified.

There are 4 fields here.

+ name: the name you want to use, it will be shown in your console

+ click_root: in each command project using Click, there must be an root command for all subcommands. The cat is the root command, so we write cat here.

+ package_path: this path indicates where is the plugin project's folder

+ package_name: this is the path from project folder to the .py file contains root command.

.. code-block:: python

    {
      "modules": [
        {
          "name": "cat",
          "click_root": "cat",
          "package_path": "../",
          "package_name" : "cat.catcli"
        }
      ]
    }


(in our example plugin_commands.json file, we also add mySQLcli and SQLlitecli to show how to add third-party plugins, if you don't need them, feel free to delete them and try our example)

2. Add plugin loader
--------------


We add the decorator loadPlugin from MetaCLI on the base command and input two parameters.

+ *json_file*: indicates where is the configuration json file
+ *base_path*: indicates where is the current file, this is helpful to do plugin as an anchor.


.. code-block:: python

    from metacli.decorators import loadPlugin

    @loadPlugin(json_file="./plugin_commands.json",
        base_path=__file__)
    @click.group()
    @click.option('--version', default = "1")
    @click.option('--verbose', default = "")
    @click.pass_context
    def dog(ctx, version, verbose) :
        """Welcome to cat's world"""


3. Collect and install all required packages
--------------

After adding the new project into base plugin, the package conflicts must be solved. So we recommend to use our dependency management to check all required packages.


Right now, *dog* is our root. So, we need to do dependency management from *dog*. Firstly, run dependency management in the console as a command line to collect all packages

.. code-block:: shell

    metacli dependency_management


The input is current plugin project's absolute path. For example, right now we are in dog, so the path will be  ```~/metacli/example/dog```. Also, you need to input the location where you want to get your requirements.txt. For example, here we also use ```~/metacli/example/dog```. After deleting conflicts in requirements.txt, you can use pip to install all required packages in one command

.. code-block:: shell

    pip install -r requirements.txt


4. Install and run CLI tools:
--------------

Now, you can install CLI tools as command click projects.

.. code-block:: shell

    # in example/dog folder

    pip install --editable .
    dog --help

Then we can see the cat command group. To construct the entire structure, just follow these 1-3 steps and get the entire structure.

5. Optional: Builtin Plugins:
--------------

We have provided some built-in plugins(shell, schema). If you want to add these plugins to any command or group. just use decorator to add them. The argument name should be "schema" or "shell" indicating help plugin or shell plugin

.. code-block:: python

    @addBuiltin(name="shell")
    @addBuiltin(name="schema")
    @loadPlugin(json_file="./plugin_commands.json",
                base_path=__file__)
    @click.group()
    @click.option('--version', default = "1")
    @click.option('--verbose', default = "")
    @click.pass_context
    def dog(ctx, version, verbose) :
        """Welcome to cat's world"""


6. Optional: Logging
--------------

MetaCLI can support logging system, please see the usage-logging for more details
