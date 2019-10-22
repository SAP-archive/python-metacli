import click
import yaml
import jinja2
import os
import pathlib
import json
from .schema import *
from .dependency_management import DependencyManagement


@click.group()
@click.pass_context
def metacli(ctx):
    """Metacli core command"""
    pass


@metacli.command("dependency_management")
@click.pass_context
def dependency_management(ctx):
    """ Perform dependency management"""
    click.echo("running dependency management")

    dm = DependencyManagement()
    dm.gather_packages_for_plugins_and_check_conflicts()



@metacli.command("create_project")
@click.option("--fromjson", help = "input your schema json file", default="")
@click.option("--fromyaml", help = "input your schema yaml file", default="")
@click.pass_context
def create_project(ctx, fromjson, fromyaml):
    """crate new project from schema.yaml or schema.json"""

    project_path = input("input project path: ")
    project_name = input("project name: ")

    if project_name == "" or project_name == "":
        raise ValueError("Empty Project Path or Project Name")

    # initial project folder
    project_path = project_path + '/' + project_name

    # initial project generator
    generator = ProjectGenerator(project_path, project_name)

    # load template engine
    parent_path = str(pathlib.Path(__file__).parent)
    loader = jinja2.FileSystemLoader(searchpath= parent_path + '/templates')
    env = jinja2.Environment(loader=loader)

    if fromjson == "" and fromyaml == "":
        # initial hello world project with cli.py, setup.py, init.py, plugin_commands.json
        templates_name = ['__init__.txt', 'setup.txt', 'cli.txt', 'plugin_commands.txt']
        templates = [env.get_template(name) for name in templates_name]

        names = ['__init__.py', 'setup.py', project_name + 'cli.py', 'plugin_commands.json']
        output, path = generator.create_empty_files(templates, names, project_name)

    else:
        # generate file based on input schema
        validator = SchemaValidator()

        if fromjson != "":
            with open(fromjson) as json_file:
                schema = json.load(json_file)
                validator.validate_json(schema)
        elif fromyaml != "":
            with open(fromyaml) as yaml_file:
                schema = yaml.load(yaml_file, yaml.FullLoader)
                validator.validate_json(schema)

        # generate cli file from data
        root_name = schema[0]['name']
        cli_output, cli_path = generator.generate_cli_from_data(env, schema, root_name)

        # generate setup.py, plugin_commands.json, __init__.py
        templates_name = ['__init__.txt', 'setup.txt', 'plugin_commands.txt']
        templates = [env.get_template(name) for name in templates_name]
        names = ['__init__.py', 'setup.py', 'plugin_commands.json']
        output, path = generator.create_empty_files(templates, names, root_name)

        # add cli.py to output
        output.append(cli_output)
        path.append(cli_path)

    # add schema.json & schema.yaml
    output, path = generator.append_schema_template(env, output, path)

    # output all files
    generator.write_files(output, path)

    # show generated file's structure
    list_files(project_path)


if __name__ == '__main__':
    metacli()
