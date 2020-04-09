from setuptools import setup

setup(
    name='yaml_project_test',
    version='0.0',
    py_modules=['yaml_project_testcli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        yaml_project_test=yaml_project_testcli:example_group
    ''',
)