import click

@click.group(name="dog", help="Welcome to dog's world", hidden=False, )
@click.option(
"--version",default="1", help=None, required=False, prompt=None, )
@click.option(
"--verbose",default="", help=None, required=False, prompt=None, )
@click.pass_context
def dog(ctx,version, verbose):
    print("this is group", "dog")
    print("parameters: ", version, verbose)



@dog.command(name="schema", help="Generate cmd structure json and get help info", hidden=False, )
@click.option(
"--display",default=False, help="show cmd structure in console", required=False, prompt=None, )
@click.pass_context
def schema(ctx,display):
    print("this is command", "schema")
    print("parameters: ", display)



@dog.command(name="shell", help="Shell ", hidden=False, )
@click.pass_context
def shell(ctx):
    print("this is command", "shell")
    print("parameters: ", )



@dog.group(name="cat", help="Welcome to cat's world", hidden=False, )
@click.pass_context
def cat(ctx):
    print("this is group", "cat")
    print("parameters: ", )



@cat.command(name="schema", help="Generate cmd structure json and get help info", hidden=False, )
@click.option(
"--display",default=False, help="show cmd structure in console", required=False, prompt=None, )
@click.pass_context
def schema(ctx,display):
    print("this is command", "schema")
    print("parameters: ", display)



@cat.command(name="welcome", help="show cat's welcome", hidden=False, )
@click.option(
"--name",default="", help="input your name", required=False, prompt=None, )
@click.pass_context
def welcome(ctx,name):
    print("this is command", "welcome")
    print("parameters: ", name)



@cat.command(name="greeting", help="Greeting from cat", hidden=False, )
@click.option(
"--name",default="", help="input your name", required=False, prompt=None, )
@click.pass_context
def greeting(ctx,name):
    print("this is command", "greeting")
    print("parameters: ", name)



@cat.group(name="ragdoll", help="Test with superman", hidden=False, )
@click.pass_context
def ragdoll(ctx):
    print("this is group", "ragdoll")
    print("parameters: ", )



@ragdoll.command(name="welcome", help="show ragdoll welcome", hidden=False, )
@click.option(
"--name",default="", help="input your name", required=False, prompt=None, )
@click.pass_context
def welcome(ctx,name):
    print("this is command", "welcome")
    print("parameters: ", name)



@ragdoll.command(name="running", help="ragdoll can run", hidden=False, )
@click.option(
"--name",default="", help="input your name", required=False, prompt=None, )
@click.pass_context
def running(ctx,name):
    print("this is command", "running")
    print("parameters: ", name)



@dog.group(name="bird", help="Many different birds are here", hidden=False, )
@click.pass_context
def bird(ctx):
    print("this is group", "bird")
    print("parameters: ", )



@bird.command(name="flying", help="bird can flying", hidden=False, )
@click.option(
"--name",default="", help="input your name", required=False, prompt=None, )
@click.pass_context
def flying(ctx,name):
    print("this is command", "flying")
    print("parameters: ", name)



@bird.command(name="dove", help="Dove is here ", hidden=False, )
@click.pass_context
def dove(ctx):
    print("this is command", "dove")
    print("parameters: ", )



@bird.group(name="bluebird", help="bluebird is here", hidden=False, )
@click.pass_context
def bluebird(ctx):
    print("this is group", "bluebird")
    print("parameters: ", )


if __name__== '__main__':
    dog()