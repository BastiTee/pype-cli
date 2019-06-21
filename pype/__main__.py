import os
import sys
import click


def _bind(plugin_name):
    print(plugin_name)
    plugin_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), plugin_name))

    class MyCLI(click.MultiCommand):

        def list_commands(self, ctx):
            print('>>', plugin_name)

            rv = []
            for filename in os.listdir(plugin_folder):
                if filename.endswith('.py') and '__' not in filename:
                    rv.append(filename[:-3])
            rv.sort()
            print(rv)
            return rv

        def get_command(self, ctx, name):
            try:
                mod = __import__('pype.' + plugin_name + '.' + name,
                                 None, None, ['cli'])
            except ImportError as e:
                print(e)
                return
            return mod.cli
    return MyCLI
    # @click.command(cls=MyCLI)
    # @click.pass_context
    # def _plugin_bind_function(ctx):
    #     print('..')
    #     pass
    # _plugin_bind_function.__name__ = plugin_name
    # click.command(cls=MyCLI)(_plugin_bind_function)
    # return _plugin_bind_function


@click.group()
@click.pass_context
def main(ctx):
    pass


# main.group()(_bind('plug1'))
# main.group()(_bind('plug2'))

@main.command(cls=_bind('plug1'))
@click.pass_context
def plug1(ctx):
    pass


if __name__ == "__main__":
    main()
