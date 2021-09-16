![](https://img.shields.io/badge/STATUS-NOT%20CURRENTLY%20MAINTAINED-red.svg?longCache=true&style=flat)

# Important Notice
This public repository is read-only and no longer maintained.

# MetaCLI

[![pypi](https://img.shields.io/pypi/v/metacli.svg)](https://pypi.python.org/pypi/metacli)
[![build](https://img.shields.io/travis/tw4dl/metacli.svg)](https://travis-ci.org/tw4dl/metacli)
[![docs](https://readthedocs.org/projects/metacli/badge/?version=latest)](https://metacli.readthedocs.io/en/latest/?badge=latest)
[![pyup](https://pyup.io/repos/github/tw4dl/metacli/shield.svg)](https://pyup.io/repos/github/tw4dl/metacli/)



Python package to build metadata driven command line tools (CLI) with out-of-the-box REST Swagger/OpenAPI support


+ Documentation: https://metacli.readthedocs.io.


## Install
```
$ git clone git@github.com:sap-staging/python-metacli.git

$ cd ./python-metacli/
$ pip install .

$ metacli --help        # Test Installation
```

## Features
+ Dynamic Plugin:
    Plugin another command project through configuration file and decorator

+ Dependency Management:
    Collect all required packages and detect conflicts & circular plugins

+ Builtin Plugin:
    + Shell: add prompt to any command level, save and retrieve parameters from different levels
    + project description: describe commands structure and arguments for any command

+ Logging
    + Logging: logging for entire command structure

+ Templates:
    + Simple Template: generate an empty command project quickly
    + Complex Template: generate an command project based on a schema design in YAML or JSON file


## Example
+ Dynamic Plugin

    In example folder, there are 3 independent command projects (cat, bird and dod). The goal is to set up a new command structure:
    ```
    dog -
        |- bird
        |- cat
    ```
    To get a quick start, the plugin_commands.json and decorators are already configured. Please check the `/example/dog/plugin_commands.json` and `/example/dog/dogcli.py` for more details.

    ```shell script
    $ cd example/dog

    $ metacli dependency_management     # install all dependencies, press enter in prompt to use current path
    $ pip install -r requirements.txt
    $ pip install --editable ./         # install new command structure

    $ dog --help        # test new command structure
    $ dog bird --help
    $ dog cat --help

    $ dog shell         # test built-in plugin shell
    $ dog schema --display       # test built-in plugin schema, generate a schema.json to describe current command structure
    ```
+ Generate new command project

    To generate a new command project which can be plugged in using MetaCLI.
    ```shell script
    $ cd example/
    $ metacli create_project          # press enter in prompt to use default path and name
    $ pip install --editable ./helloworld
    $ helloworld --help
    ```

    To generate a new command project from metadata which can be plugged in using MetaCLI.
    ```shell script
    $ cd example/
    $ metacli create_project --fromjson schema.json   # press enter in prompt to use default path and name
    # or metacli create_project --fromyaml schema.yaml
    $ pip install --editable ./helloworld
    $ helloworld --help
    ```


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

## Known Issues

There are no known issues.

## How to Obtain Support

This project is provided as is.

## License

Copyright (c) 2020 SAP SE or an SAP affiliate company. All rights reserved.
This file is licensed under the Apache Software License, v. 2 except as noted otherwise in the [LICENSE](LICENSE) file.

