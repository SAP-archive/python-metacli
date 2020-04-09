import click
from .shell import Shell
from .schema import SchemaInfoGenerator


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
    schema_generator = SchemaInfoGenerator()
    schema_generator.get_help_info(root, display=display)
