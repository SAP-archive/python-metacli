import click

@click.group()
@click.pass_context
def empty_project_test(ctx):
    """empty_project_test"""
    pass

@empty_project_test.command()
@click.pass_context
def hello_world(ctx):
    print("hello world", 'empty_project_test')
