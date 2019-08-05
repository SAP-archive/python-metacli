from setuptools import setup

setup(
    name='core',
    version='0.0',
    py_modules=['cli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        core=cli:core
    ''',
)
