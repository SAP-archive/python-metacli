import click
import yaml
import jinja2
import os
import pathlib
import json
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


@metacli.command("convert")
@click.option("--fromjson", help = "input your schema json file", default="")
@click.option("--fromyaml", help = "input your schema yaml file", default="")
@click.pass_context
def converter(ctx, fromjson, fromyaml):
    """convert from json to yaml or yaml to json"""
    if fromjson != "":
        with open(fromjson, 'r') as f:
            data = json.load(f)

        with open('test.yaml', 'w') as f:
            yaml.dump(data, f)
    if fromyaml != "":
        with open(fromyaml, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        with open('test2.json', 'w') as f:
            json.dump(data, f, indent=2)


@metacli.command("create_project")
@click.option("--fromjson", help = "input your schema json file", default="")
@click.option("--fromyaml", help = "input your schema yaml file", default="")
@click.pass_context
def create_project(ctx, fromjson, fromyaml):
    """crate new project from schema.yaml or schema.json"""

    project_path = input("input project path: ")
    project_name = input("project name: ")

    if project_name == "" or project_name == "":
        raise ValueError("Empty Input")

    # initial project folder
    project_path = project_path + '/' + project_name

    if os.path.exists(project_path):
        delete = input("Already Existed, would you want to replace? y/n \n")
        if delete == 'y' or delete == 'Y':
            clean_project(project_path)
        else:
            raise FileExistsError

    os.mkdir(project_path)

    # load template
    parent_path = str(pathlib.Path(__file__).parent)
    loader = jinja2.FileSystemLoader(searchpath= parent_path + '/templates')
    env = jinja2.Environment(loader=loader)

    if fromjson == "" and fromyaml == "":
        # initial empty project with cli.py, setup.py, init.py, plugin_commands.json
        templates_name = ['__init__.txt', 'setup.txt', 'cli.txt', 'plugin_commands.txt']
        templates = [env.get_template(name) for name in templates_name]

        names = ['__init__.py', 'setup.py', project_name + 'cli.py', 'plugin_commands.json']
        output, path = create_empty_files(templates, names, project_name, project_path, project_name)

    else:
        if fromjson != "":
            with open(fromjson) as json_file:
                schema = json.load(json_file)
        elif fromyaml != "":
            with open(fromyaml) as yaml_file:
                schema = yaml.load(yaml_file)

        # generate cli file
        # generate cli body
        cli_template = env.get_template('cli_body.txt')

        cli_body_output = ""
        cli_body_output += parse_cli(None, schema, cli_template)

        # add header and end to cli
        root_name = schema[0]['name']
        cli_start_template = env.get_template("cli_start.txt")
        cli_end_template = env.get_template("cli_end.txt")
        cli_output = cli_start_template.render() + cli_body_output + cli_end_template.render(root=root_name)
        cli_path = project_path + '/' + project_name +'cli.py'

        # add setup.py, plugin_commands.json, __init__.py
        templates_name = ['__init__.txt', 'setup.txt', 'plugin_commands.txt']
        templates = [env.get_template(name) for name in templates_name]
        names = ['__init__.py', 'setup.py', 'plugin_commands.json']
        output, path = create_empty_files(templates, names, project_name, project_path, root_name)

        # add cli.py
        output.append(cli_output)
        path.append(cli_path)


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
