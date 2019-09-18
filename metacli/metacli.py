import click
import jinja2
import os
import pathlib
from .schema import *
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


@metacli.command("initial")
@click.pass_context
def initial(ctx):
    project_path = input("input project path: ")
    project_name = input("project name: ")

    if project_name == "" or project_name == "":
        raise ValueError("Empty Input")

    # initial project folder
    project_path = project_path + '/' + project_name

    if os.path.exists(project_path):
        delete = input("Already Existed, would you want to replace?")
        if delete == 'y':
            clean_project(project_path)
        else:
            raise FileExistsError

    os.mkdir(project_path)

    # load template
    parent_path = str(pathlib.Path(__file__).parent)
    loader = jinja2.FileSystemLoader(searchpath= parent_path + '/templates')
    env = jinja2.Environment(loader=loader)

    # initial cli.py, setup.py, init.py, plugin_commands.json
    cli_output, cli_path = initial_file(template = env.get_template('cli.txt'),
                                        name = project_name + 'cli.py',
                                        project_name = project_name,
                                        project_path = project_path)

    setup_output, setup_path = initial_file(template = env.get_template('setup.txt'),
                                            name = 'setup.py',
                                            project_name = project_name,
                                            project_path = project_path)

    init_output, init_path = initial_file(env.get_template('__init__.txt'),
                                          name = '__init__.py',
                                          project_name=project_name,
                                          project_path=project_path)

    plugin_json_output, plugin_json_path = initial_file(template = env.get_template('plugin_commands.txt'),
                                                        name = 'plugin_commands.json',
                                                        project_path = project_path,
                                                        project_name = project_name)

    # write all templates into files
    output = [cli_output, setup_output, init_output, plugin_json_output]
    path = [cli_path, setup_path, init_path, plugin_json_path]

    try:
        for output, file in zip(output, path):
            with open(file, 'w') as f:
                f.write(output)
    except Exception as e:
        print(e)
        if os.path.exists(project_path):
            clean_project(project_path)
            print("cleaned project")

    # display structure
    list_files(project_path)

if __name__ == '__main__':
    metacli()
