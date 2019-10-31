# Changelog

## Version 0.3.7

- run_interactive and run_and_get_output now always shell=True
- Combine make-extension and make
- Fix help for --unregister-alias
- Document example pypes
- Update pype-cli documentation
- Add terminalizer for resources

## Version 0.3.6

- Fix bug in pype.config.shell-install
- Source complete script for zsh and bsh only once
- Split complete files for bash and zsh
- Improve init-file creation

## Version 0.3.5

- Fix simplified process for custom shell command

## Version 0.3.4

- Simplified process for custom shell command
- Improve README

## Version 0.3.3

- Add auto creation for empty config filepaths
- Improved development workflow
- Fix fallback to VISUAL or EDITOR mode on opening pypes
- Fix bug for pypes relative to configuration file
- Fix print-out bug in pype deletion
- Improved template pype
- Add .env file for editor support

## Version 0.3.2

- NaN

## Version 0.3.1

- Add dynamic subcommand routine
- Allow one-tab completion for bash-environments
- Hide stacktrace on unknown plugin-pype
- Fix linux installation
- Refine dependency installation

## Version 0.3.0

- Rewrite `__main__` procedure now using click multicommands instead of spawning a new subshell, which allows much better dynamic chaining of pypes
- Reduce complexity of install shell by writing to all available rc files
- Update all print() calls with category-sensitive versions
- Normalize plugin paths if plugin is relative to config.json
- Normalize plugin paths if relative to make file
- Normalize plugin paths to save homefolder as tilde if used
- Improve metavars on scripts
- Rename 'commands' section in help pages to 'plugins' and 'pypes'
- Fixed dockerfile
- Fix pype.config version when sourced instead of being called directly
- Rename query_yes_no to ask_yes_or_no, query_text to ask_for_text
- Relocate ask_yes_no and ask_for_text to new cli package
- Refine setup.cfg
- Switch from git submodule behaviour to git subtree
- Refine linting for W503 and W504
- Ignore Q003 on flake8 linter
- Refine pype --list
- Add pype --aliases

## Version 0.2.0

- Extended pype.config.system-info
- Alternative shell command (instead of `pype`)  configurable via config file entry `core_config.shell_command`
- Normalization of command names
- Add flake8-blind-except linter
- Make keyboard interrupt silent on subprocess
- Internal class renaming for consistency

## Version 0.1.2

- Add <https://pypi.org/project/progress/> as external dependency
- Refine `pype --list`
- Add `pype pype.config system-info`
- Add `make profile` to benchmark runtime performance
- Fix docker image for mint-installation testing

## Version 0.1.1

- Fixed missing jsonschema dependency in setup.py

## Version 0.1.0

- Stabilized interfaces
- Added configuration file schema validation using jsonschema
- Support extended to Python >=3.5
- Extended linter configuration
