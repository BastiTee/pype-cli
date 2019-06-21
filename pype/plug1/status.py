import click
# from complex.cli import pass_context


@click.command('status', short_help='Shows file changes.')
def cli():
    """Shows file changes in the current working directory."""
    # ctx.log('Changed files: none')
    # ctx.vlog('bla bla bla, debug info')
    print('status called')
