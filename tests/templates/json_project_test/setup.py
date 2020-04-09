from setuptools import setup

setup(
    name='json_project_test',
    version='0.0',
    py_modules=['json_project_testcli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        json_project_test=json_project_testcli:dog
    ''',
)