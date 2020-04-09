from setuptools import setup

setup(
    name='ragdoll',
    version='0.1',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        ragdoll=cli:ragdoll
    ''',
)
