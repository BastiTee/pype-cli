# pype

> A command-line tool for command-line tools

## Development

- Run `./make shell` to open a `pipenv` shell with the required shell configuration
- Inside venv-shell run `pype` to operate locale development version (it will react to code changes)

## To-Do's

This project is currently a proof of concept.

- [ ] Auto-complete custom pypes using Click
- [ ] Allow separation of subcommand options and pype-internal options (e.g. `-h` option)
- [ ] Move example pypes to dedicated folder and make path configurable
- [x] Find a way to re-use module/script documentation for CLI documentation
- [x] Introduce verbosity option
- [x] Introduce a logging framework
- [x] Add auto-listing of configured pypes
- [x] Allow configuring custom pypes via configuration file
- [x] Introduce configuration file
- [x] Check how to backward-support shell scripts
- [x] Setup with python3 best-practices boilerplate
