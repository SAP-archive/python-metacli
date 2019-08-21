import click
from metacli.decorators import addBuiltin


@addBuiltin(name="shell")
@click.group(invoke_without_command=True)
@click.pass_context
def test(ctx):
    ''' Test '''

    if ctx.obj:
        return

    ctx.obj = {}



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
    click.echo('Verbosity: %s' % s)


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
    click.echo(rv)

@test.command()
@click.option('--n', default=1)
@click.pass_context
def dots(ctx, n):
    click.echo('.' * n)

@test.command()
@click.option('--pos', nargs=2, type=float)
@click.pass_context
def findme(ctx, pos):
    click.echo('%s / %s' % pos)

@test.command()
@click.option('--item', type=(str, int))
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
    click.echo(ctx.obj)
    click.echo("version: %s" % ctx.obj["version"])


@counting.command()
@click.option('--s', default= "")
@click.pass_context
def save(ctx, s):
    click.echo("save")
    click.echo('Verbosity: %s' % s)


@counting.command()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def log(ctx, verbose):
    click.echo("log")
    click.echo('Verbosity: %s' % verbose)


if __name__ == "__main__":
    test()
