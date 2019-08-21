from setuptools import setup

setup(
    name='testing_shell',
    version='0.1',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        testshell=testsh:test
    ''',
)
