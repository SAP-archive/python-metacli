import click
from metacli.decorators import addBuiltin
from metacli.util import set_context_obj

@addBuiltin(name="shell")
@click.group()
@click.option('--version', default = "")
@click.pass_context
def test(ctx, version):
    ''' Test '''

    set_context_obj(ctx)

    ctx.obj['version'] = version
    click.echo("in test")
    click.echo("version: %s" % version)

@test.command()
@click.pass_context
def print(ctx):
    click.echo("in print")
    click.echo("version: %s" % ctx.obj["version"])


@test.command(hidden=False)
@click.option('--foo', required=True)
@click.pass_context
def a(ctx, foo):
    click.echo("a")
    click.echo(foo)
    return 'banana'


@test.command(hidden=False)
@click.pass_context
def c(ctx):
    click.echo("c")



@test.command(hidden=False)
@click.option('--foo', required=True)
@click.pass_context
def b(ctx, foo):
    click.echo("b")
    click.echo(foo)



@test.command()
@click.option('--s', default= "")
@click.pass_context
def save(ctx, s):
    click.echo("save")
    click.echo('msg: %s' % s)


@test.command()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def log(ctx, verbose):
    click.echo("log")
    click.echo('Verbosity: %s' % verbose)


@test.command()
@click.option('--shout/--no-shout', default=False)
@click.pass_context
def info(ctx, shout):
    rv = "test"
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)

@test.command()
@click.option('--shout', is_flag=True)
@click.pass_context
def info2(ctx, shout):
    rv = "test"
    if shout:
        rv = rv.upper() + '!!!!111'
    else:
        print("nope")
    click.echo(rv)

@test.command()
@click.option('--n', default=1)
@click.option('--m', default="")
@click.pass_context
def dots(ctx, n, m):
    click.echo('.' * n)
    click.echo(m)

@test.command()
@click.option('--pos', nargs=2, type=float)
@click.pass_context
def findme(ctx, pos):
    click.echo('%s / %s' % pos)

@test.command()
@click.option('--item', type=(str, int), default=("yi", 1))
@click.pass_context
def putitem(ctx, item):
    click.echo('name=%s id=%d' % item)


@test.command()
@click.option('--message', '-m', multiple=True)
@click.pass_context
def commit(ctx, message):
    click.echo('\n'.join(message))

@test.group("yi_group")
@click.pass_context
def yi_group(ctx):
    click.echo("in yi group")

@yi_group.command("hi")
@click.pass_context
def hi(ctx):
    click.echo("hello ;D")


@test.group("counting")
@click.option('--version', default = "")
@click.pass_context
def counting(ctx, version):
    ctx.obj['version'] = version
    click.echo("in counting")
    click.echo("version: %s" % version)


@counting.command()
@click.pass_context
def print(ctx):
    click.echo("version: %s" % ctx.obj["version"])


@counting.command()
@click.option('--s', default= "")
@click.pass_context
def save(ctx, s):
    click.echo("save")
    click.echo('msg: %s' % s)


@counting.command()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def log(ctx, verbose):
    click.echo("log")
    click.echo('Verbosity: %s' % verbose)

@test.group("apictl")
@click.option('--verbose', default = "")
@click.pass_context
def apictl(ctx, verbose):

    ctx.obj['verbose'] = verbose
    click.echo("in apictl")
    click.echo("version: %s" % ctx.obj["version"])
    click.echo("verbose: %s" % verbose)

@apictl.command()
@click.pass_context
def print(ctx):
    click.echo("in print")
    click.echo("version: %s" % ctx.obj["version"])
    click.echo("verbose: %s" % ctx.obj["verbose"])

@apictl.group("datacenter")
@click.option('--dc', default = "")
@click.pass_context
def datacenter(ctx, dc):
    ctx.obj['dc'] = dc
    click.echo("in datacenter")
    click.echo("version: %s" % ctx.obj["version"])
    click.echo("verbose: %s" % ctx.obj["verbose"])
    click.echo("dc: %s" % dc)


@datacenter.command()
@click.pass_context
def print(ctx):
    click.echo("in print")
    click.echo("version: %s" % ctx.obj["version"])
    click.echo("verbose: %s" % ctx.obj["verbose"])
    click.echo("dc: %s" % ctx.obj["dc"])

if __name__ == "__main__":
    test()
