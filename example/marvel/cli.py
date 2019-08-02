import click

@click.group(invoke_without_command=True)
@click.pass_context
def marvel(ctx):
    """Test with marvel superherors"""
    pass

@click.option("--name",
              help="input your name",
              default="")

@marvel.command("welcome")
@click.pass_context
def marvel_welcome(ctx, name):
    """show marvel welcome"""
    click.echo("Hello " + name +  " Marvel World ")


@marvel.group("ironman")
@click.pass_context
def ironman(ctx):
    """Ironman"""


@ironman.command("welcome")
@click.pass_context
def ironman_welcome(ctx):
    """show ironman """
    click.echo("Hello Ironman under marvel")



"""
test duplicate group names in different levels (a under marvel, a under marvel->ironman)
group structure:
    marvel
    |
    -- ironman
    |  |
    |  -- a
    |  
    -- a      
    
test duplicate command names in different levels (welcome under marvel, welcome under marvel->ironman )
command structure:
    marvel
    |
    -- ironman
    |  |
    |  -- a
    |     |
    |      -- command: welcome
    |  
    -- a
    |  |
    |  -- command: welcome      
"""

########################

@marvel.group("a")
@click.pass_context
def a(ctx):
    """a under marvel"""

@a.command("welcome")
@click.pass_context
def a_welcome(ctx):
    """show a """
    click.echo("Hello a under marvel")


#########################
@ironman.group("a")
@click.pass_context
def a(ctx):
    """a under ironman"""

@a.command("welcome")
@click.pass_context
def a_welcome(ctx):
    """show a """
    click.echo("Hello a under ironman")
