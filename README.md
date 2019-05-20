# pype

> A command-line tool for command-line tools

## Development usage

- Run `./make shell` to open a `pipenv` shell with the required shell configuration
- Run `pype` to operate locale development version (it will react to code changes)

## To-Do's

This project is currently a proof of concept.

- [ ] Allow aliasing of pype chains
- [ ] Allow creating plugins on the fly
- [ ] Validate config.json before using it (see <https://pypi.org/project/jsonschema/>)
- [x] Extend documentation of template pype
- [x] Add help texts to commands
- [x] Auto-install bash/zsh completion
- [x] Find another name since pype is unavailable in PyPi `¯\_(ツ)_/¯`
- [x] Improve config file resolving to envvar->homefile->currdir->default
- [x] Add option to add/delete plugins via pype
- [x] Add option to create a new pype via pype
- [x] Add option to open a pype in default browser
- [x] Internalize default pypes such as 'version'
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
