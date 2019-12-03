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

pip metacli/

```

## Features
+ Dynamic Plugin:
    Plugin another command project within 1 line code

+ Dependency Management:
    Collect all required packages and detect conflicts & deadloop in plugin command project
    
+ Builtin Plugin:
    + Shell: add prompt to any command level, save and retrieve parameters from different levels
    + project description: describe commands structure and arguments for any command
    
+ Templates:
    + Simple Template: generate an empty command project quickly
    + Complex Template: generate an command project based on a schema design in YAML or JSON file
    

## Links:
Doc: <please compile docs/ ans see preview doc>
    
## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.



