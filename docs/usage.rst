.. highlight:: shell

=====
Usage
=====

Describe Schema
--------------



Simple Templates
--------------
We provide templates to help user create their own command line project easily.

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
--------------

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







