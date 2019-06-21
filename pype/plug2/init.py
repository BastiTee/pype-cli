import click
# from complex.cli import pass_context


@click.command('init', short_help='Initializes a repo.')
@click.argument('path', required=False, type=click.Path(resolve_path=True))
def cli(path):
    """Initializes a repository."""
    print('init called')
