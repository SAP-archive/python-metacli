from setuptools import setup

setup(
    name='marvel',
    version='0.1',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        marvel=cli:marvel
    ''',
)
