.. highlight:: shell

============
Getting Start
============
Here is an simple example to help you getting start.

In example folder, we have 4 independent projects. The file structure is:

| -- bird\
| -- cat\
|   |-- ragdoll\
| -- dog

All projects are the simplest command line project based on Click, which means you can run them independently.

Now, The goal is to construct a command line structure like:

-- dog \
  |-- cat \
    |--ragdoll\
  |-- bird\


Now let's to do this step by step.

1. Configure json file to construct structure
--------------

Firstly, we want to plug *cat* into *dog*. So, the example/dog/plugin_commands.json needs to be modified.

There are 4 fields here.

+ name: the name you want to use for this command, it will be shown in your console

+ click_root: For each project using Click, there must be an root command for all subcommands. The cat is the root command here.

+ package_path: this path indicates where is the plugin project's folder

+ package_name: this is the path from project folder to the .py file contains root command.

.. code-block:: python

    {
      "modules": [
        {
          "name": "cat",
          "click_root": "cat",
          "package_path": "../cat/",
          "package_name" : "catcli"
        }
      ]
    }


(in our example plugin_commands.json file, we also add `MySQLcli <https://github.com/dbcli/mycli>`_ and
`SQLlitecli <https://github.com/dbcli/litecli>`_ to show how to add real plugins, if you don't need them, feel free to delete them and try our example)

2. Add plugin loader
--------------


We add the decorator loadPlugin from MetaCLI on the base command and input two parameters.

+ *json_file*: indicates where is the configuration json file
+ *base_path*: indicates where is the current file, this is helpful to do plugin as an anchor.


.. code-block:: python

    from metacli.decorators import loadPlugin

    @loadPlugin(json_file="plugin_commands.json",
        base_path=__file__)
    @click.group()
    @click.option('--version', default = "1")
    @click.option('--verbose', default = "")
    @click.pass_context
    def dog(ctx, version, verbose) :
        """Welcome to cat's world"""
        pass


3. Collect and install all required packages
--------------

After adding the new project into base plugin, the package conflicts must be solved. So we recommend to use our dependency management to check all required packages.


Right now, *dog* is our root. So, we need to run dependency management inside *dog*. Firstly, run dependency management in the console to collect all packages

.. code-block:: shell

    metacli dependency_management


The default path is current path, so we can just press enter in prompt, MetaCLI will use current path to collect packages and generate requirement.txt.

(If you want to input by yourself, please use absolute path here.  For example, here we use ```~/metacli/example/dog```.)

After deleting conflicts in requirements.txt, you can use pip to install all required packages in one command

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

We have provided some built-in plugins(shell, schema). If you want to add these plugins to any command or group. just use decorator to add them. The argument name should be "schema" or "shell".

.. code-block:: python

    @addBuiltin(name="shell")
    @addBuiltin(name="schema")
    @loadPlugin(json_file="plugin_commands.json",
                base_path=__file__)
    @click.group()
    @click.option('--version', default = "1")
    @click.option('--verbose', default = "")
    @click.pass_context
    def dog(ctx, version, verbose) :
        """Welcome to cat's world"""
        pass


