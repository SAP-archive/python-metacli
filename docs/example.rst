.. highlight:: shell
.. _example-doc:

============
Getting Start
============
In example folder, there are 3 independent command projects (cat, bird and dod). The goal is to set up a new command structure:


::    dog
        - bird
        - cat


All projects are the minimal command line project based on Click, which means they can be run independently.


1. Configure json file to set up structure
--------------

Firstly, to plug *cat* into *dog*, the example/dog/plugin_commands.json needs to be modified.

There are 4 fields here.

+ name: the name you want to use for this command, it will be shown in console

+ click_root: For each project using Click, there must be an root command for all subcommands or subgroups. The cat is the root command here.

+ package_path: this path indicates where is the plugin project's folder

+ package_name: this is the path from project folder to the python file contains root command.

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

To show how to add other plugins on Github like `MySQLcli <https://github.com/dbcli/mycli>`_ and `SQLlitecli <https://github.com/dbcli/litecli>`_:

.. code-block:: python

    {
      "name": "litesql",
      "click_root": "cli",
      "package_path": "../litecli/",
      "package_name" : "litecli.main"
    },
    {
      "name": "mysql",
      "click_root": "cli",
      "package_path": "../mycli/",
      "package_name" : "mycli.main"
    }



2. Add plugin loader
--------------

The next step is to add plugin loader into *dog* project. In dog/dogcli.py, there are two arguments for the loader:

+ *json_file*: indicates where is the configuration json file relative to base path.
+ *base_path*: indicates where is the current file, this is helpful to do plugin as an anchor, recommend using __file__ here.


.. code-block:: python

    from metacli.decorators import loadPlugin

    @loadPlugin(json_file="plugin_commands.json",
        base_path=__file__)
    @click.group()
    @click.option('--version', default = "1")
    @click.option('--verbose', default = "")
    @click.pass_context
    def dog(ctx, version, verbose) :
        """Welcome to dog's world"""
        pass


3. Collect and install all required packages
--------------

After adding the new project into base plugin, the package conflicts must be solved. So the dependency management tools in MetaCLI is recommended to check all required packages.


Right now, *dog* is our root. So, the following command needs to be run under the /dog folder. We can press enter in prompt to use current path as default for convenient, or we can input the absolute path for the project.

.. code-block:: shell

    metacli dependency_management


MetaCLI will use current path to collect packages and generate requirement.txt.

After editing and deleting conflicts in requirements.txt, all the required packages can be installed using:

.. code-block:: shell

    pip install -r requirements.txt


4. Install and run CLI tools:
--------------

The new command structure is set up and can be installed:

.. code-block:: shell

    # in example/dog folder

    pip install --editable .
    dog --help

 Now, the cat command is shown as a subcommand under the dog. To construct the entire structure, just follow 1-2 steps for bird and get the entire structure.

5. Others
--------------

+ built-in plugin: see :ref:`built-in-plugin-doc`

+ new project generator: see :ref:`new-project-generator`

+ logging: :ref:`logging-doc`


