from setuptools import setup

setup(
    name='dog',
    version='0.0',
    py_modules=['cli'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        dog=dogcli:dog
    ''',
)
