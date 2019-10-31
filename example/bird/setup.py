from setuptools import setup

setup(
    name='bird',
    version='0.1',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        bird=birdcli:bird
    ''',
)
