# pype

> A command-line tool for command-line tools

## Development

- Run `./make shell` to open a `pipenv` shell with the required shell configuration
- Inside venv-shell execute `eval "$(_PYPE_COMPLETE=source pype)"` for bash-completion
- Run `pype` to operate locale development version (it will react to code changes)

## To-Do's

This project is currently a proof of concept.

- [ ] Internalize default pypes such as 'version'
- [ ] Transfer bash completion fixes etc to post-install step
- [x] Create a docker image to test installation on a mint system
- [x] Auto-complete custom pypes using Click
- [x] Allow separation of subcommand options and pype-internal options (e.g. `-h` option)
- [x] Move example pypes to dedicated folder and make path configurable
- [x] Find a way to re-use module and script documentation for CLI documentation
- [x] Introduce verbosity option
- [x] Introduce a logging framework
- [x] Add auto-listing of configured pypes
- [x] Allow configuring custom pypes via configuration file
- [x] Introduce configuration file
- [x] Check how to backward-support shell scripts
- [x] Setup with python3 best-practices boilerplate

## Important resources

- <https://click.palletsprojects.com/en/7.x/>
- <http://click.palletsprojects.com/en/7.x/commands/>
- <https://click.palletsprojects.com/en/7.x/bashcomplete/>
- <https://click.palletsprojects.com/en/7.x/api/#click.Context>
