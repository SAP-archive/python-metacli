from setuptools import setup

setup(
    name='cat',
    version='0.1',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        cat=catcli:cat
    ''',
)
