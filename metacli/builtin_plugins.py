#from click_repl import repl

import click
from .util import get_help_info
from .shell import Shell
import os
import time


@click.command("shell")
def shell():
    """ Shell """
    root_command = click.get_current_context().__dict__['parent'].__dict__['command']
    root_ctx = click.Context(root_command)
    repl = Shell(root_ctx, root_shell=True)
    repl.cmdloop()


@click.command('schema')
@click.option('--display', is_flag=True, help='show cmd structure in console')
@click.pass_context
def schema(ctx, display):
    """Generate cmd structure json and get help info"""
    # get parent object
    root = click.get_current_context().__dict__['parent'].__dict__['command']
    get_help_info(root, display=display)

@click.command('login')
@click.pass_context
def login(ctx):
    """Permission Control Login"""
    username = input("Input username: ")
    password = input('Input Password: ')


    #TODO: Verification

    with open(".temp.txt", "w+") as f:
        f.write("$".join([username, str(time.time())]))

@click.command('logout')
@click.pass_context
def logout(ctx):
    """Permission Control Logout"""
    if os.path.exists(".temp.txt"):
        os.remove(".temp.txt")
        click.echo("Logout Successful")
