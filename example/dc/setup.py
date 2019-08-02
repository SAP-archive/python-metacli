from setuptools import setup

setup(
    name='dc',
    version='0.1',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        dc=cli:dc
    ''',
)
