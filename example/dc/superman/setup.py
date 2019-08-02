from setuptools import  setup

setup(
    name='superman',
    version='0.1',
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        superman=cli:superman
    ''',
)
