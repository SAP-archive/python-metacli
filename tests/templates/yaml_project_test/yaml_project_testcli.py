import click

@click.group(name="example_group", help="This is an schema example to show how to write a group schema", hidden=False, )
@click.pass_context
def example_group(ctx):
    print("this is group", "example_group")
    print("parameters: ", )



@example_group.command(name="example_command", help="This is an schema example to show how to write a command schema", hidden=False, )
@click.option(
"--example_argument",default=False, help="This is an schema example to show how to write an option", required=False, prompt=None, )
@click.pass_context
def example_command(ctx,example_argument):
    print("this is command", "example_command")
    print("parameters: ", example_argument)


if __name__== '__main__':
    example_group()