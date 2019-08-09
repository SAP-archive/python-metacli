import click
from .dependency_management import DependencyManagement


@click.group(help='This tool is shared library')
@click.pass_context
def metacli(ctx):
    """Test with apictl core"""
    pass


@metacli.command("dependency_management")
@click.pass_context
def dependency_management(ctx):
    """ Perform dependency management"""
    click.echo("running dependency management")

    dm = DependencyManagement()
    dm.gather_packages_for_plugins_and_check_conflicts()

if __name__ == '__main__':
    metacli()
