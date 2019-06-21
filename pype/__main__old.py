#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pype main entry point."""


def _bind_plugin(name, plugin):
    @click.option('--create-pype', '-c',
                  help='Create new pype with provided name')
    @click.option('--minimal', '-m', is_flag=True,
                  help='Use a minimal template with less boilerplate '
                  + '(only used along with "-c" option')
    @click.option('--edit', '-e', is_flag=True,
                  help='Open new pype immediatly for editing '
                  + '(only used along with "-c" option')
    @click.option('--delete-pype', '-d',
                  help='Deletes pype for provided name')
    @click.option('--open-pype', '-o',
                  help='Open selected pype in default editor')
    @click.pass_context
    def _plugin_bind_function(
            ctx, create_pype, minimal, edit, delete_pype, open_pype):
        if (minimal or edit) and not create_pype:
            print_error(
                '"-m" and "-e" can only be used with "-c" option.')
            print_context_help(ctx, level=2)
            return
        toggle_invoked = False
        if create_pype:  # Handle creation of pypes
            created_pype_abspath = PYPE_CORE.create_pype_or_exit(
                create_pype, plugin, minimal)
            toggle_invoked = True
        if delete_pype:  # Handle deletion of pypes
            PYPE_CORE.delete_pype(delete_pype, plugin)
            toggle_invoked = True
        if open_pype or edit:  # Handle opening existing or new pypes
            if plugin.internal:
                print_error('Opening internal pypes is not supported.')
                return
            # Resolve either an existing or a newly created pype
            pype_abspath = (PYPE_CORE.get_abspath_to_pype(
                plugin, sub('-', '_', open_pype))
                if open_pype else created_pype_abspath)
            if not pype_abspath:
                print_error(
                    'Pype "{}" could not be found.'.format(open_pype))
                return
            open_with_default(pype_abspath)
            toggle_invoked = True
        # Handle case that no toggles were used and no commands selected
        if not toggle_invoked and not ctx.invoked_subcommand:
            print_context_help(ctx, level=2)
    _plugin_bind_function.__name__ = _normalize_command_name(name)
    return _plugin_bind_function


def _bind_pype(name, plugin, pype):
    @click.pass_context
    @click.argument('extra_args', nargs=-1, type=click.UNPROCESSED)
    @click.option('--help', '-h', is_flag=True)
    def _pype_bind_function(ctx, extra_args, help):  # noqa: A002
        if ctx.parent.parent.register_alias:
            PYPE_CORE.register_alias(
                ctx, extra_args, ctx.parent.parent.register_alias)
            return
        # else spawn selected pype
        syspath.append(path.dirname(plugin.abspath))
        sub_environment = environ.copy()
        sub_environment['PYTHONPATH'] = ':'.join(syspath)
        extra_args = ['--help'] if help else list(ctx.params['extra_args'])
        command = [executable, '-m', plugin.name
                   + '.' + pype.name] + extra_args
        try:
            subprocess.run(command, env=sub_environment)
        except KeyboardInterrupt:
            pass  # Be silent if keyboard interrupt was catched
    _pype_bind_function.__name__ = _normalize_command_name(name)
    return _pype_bind_function


# Go through all configured plugins and their pypes and setup command groups
for plugin in PYPE_CORE.get_plugins():
    _plugin_bind_function = _bind_plugin(plugin.name, plugin)
    plugin_click_group = main.group(
        invoke_without_command=True, help=plugin.doc)(
            _plugin_bind_function)
    ctx_settings = dict(
        ignore_unknown_options=True,
        allow_extra_args=True
    )
    for pype in plugin.pypes:
        plugin_click_group.command(
            context_settings=ctx_settings, help=pype.doc)(
            _bind_pype(pype.name, plugin, pype))


if __name__ == '__main__':
    main()
