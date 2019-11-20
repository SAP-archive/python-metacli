from setuptools import setup

setup(
    name='empty_project_test',
    version='0.0',
    py_modules=['empty_project_testcli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        empty_project_test=empty_project_testcli:empty_project_test
    ''',
)