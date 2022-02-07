# Changelog

## 0.7.0

- Rename PypeException to PypeError
- Update of all libraries

## 0.6.7

- Hotfix for bug in dependency management

## 0.6.6

- Codebase clean up

## 0.6.5

- Type-safe Configuration object everywhere
- Merge pull request #12 from BastiTee/feature/type-safe-configuration

## 0.6.4

- New release process

## 0.6.2

- Simplify build and release process via Github actions

## 0.6.1

- Activate mypy for full code base
- Harden plugin resolving
- Fix dependency statements
- Fix broken pype pype.config.logger
- Rename test helpers to not confuse pytest
- Add tests for config_model

## 0.6.0

- Source code now fully typed and typings ensured via mypy
- Extended 'pype pype.config system-info' with venv infos
- Removed 'pype pype.config version'
- Fixed .env file configuration for PyLance
- Fixed .venv discovery and configuration file handling
- Added pype-cli as editable for .venv development
- Ensure system configuration file is not tampered with
- Added mypy build process
- Lean setup.py and lower python bound 3.7
- Add vscode extensions recommendations

## 0.5.5

- Clean up templates

## 0.5.4

- Fix template.py

## 0.5.3

- Fix open formatting and Makefile issues
- Add documentation how to show benchmark information

## 0.5.2

- Add load time benchmarking using `PYPE_BENCHMARK_INIT=1` as trigger variable
- Replace make script with Makefile
- Replace Travis CI with GitHub actions
- Upgrade build environment

## 0.5.1

- Complete `pype <plugin> --open-pype <pype>`

## 0.5.0

- Functionality

  - Store configurations in a ~/.pype folder instead of separate files
  - Add logging capabilities that are saved in configuration file
  - Remove mechanism that resolves plugins relative to configuration file (too complex)
  - Disallow re-registering of plugin with same name
  - Autocomplete pype names on `--delete-pype` option for each plugin
  - Autocomplete aliases on `pype --aliases-unregister`
  - Autocomplete plugins on `pype pype.config plugin-unregister`
  - Flip option name for `pype --register-alias` and `pype --unregister-alias`

- Development

  - Make pype .venv-aware to support system-independent development
  - Fix bash-setup for venv

- Code improvements

  - Remove facading of config handler in core

## 0.4.1

- Add [short aliases](pype/__init__.py) for run_interactive and run_and_get_output

## 0.4.0

- Breaking changes

  - Remove unused code in util package
  - Introduce pype-cli [import facade](pype/__init__.py) to be able to only import pype

- Code improvements

  - Add support for Python 3.8
  - Better catch bad JSON configuration file
  - Heavily extended integration tests
  - Fix a handful of errors in CLI-documentation
  - Remove obsolete package imports

- Build process

  - Remove tox.ini since it is not used
  - Fix command line linter

- Documentation

  - Add GIF to README for better documentation
  - Add example script in 'basics' plugin that is 100% independent from pype-cli
  - Document that pypes are not bound to be used in pype-cli
  - Extend documentation of example pypes
  - Reference click in documentation to highlight heavy usage
  - Reference templates in example documentation

## 0.3.7

- run_interactive and run_and_get_output now always shell=True
- Combine make-extension and make
- Fix help for --unregister-alias
- Document example pypes
- Update pype-cli documentation
- Add terminalizer for resources

## 0.3.6

- Fix bug in pype.config.shell-install
- Source complete script for zsh and bsh only once
- Split complete files for bash and zsh
- Improve init-file creation

## 0.3.5

- Fix simplified process for custom shell command

## 0.3.4

- Simplified process for custom shell command
- Improve README

## 0.3.3

- Add auto creation for empty config filepaths
- Improved development workflow
- Fix fallback to VISUAL or EDITOR mode on opening pypes
- Fix bug for pypes relative to configuration file
- Fix print-out bug in pype deletion
- Improved template pype
- Add .env file for editor support

## 0.3.2

- NaN

## 0.3.1

- Add dynamic subcommand routine
- Allow one-tab completion for bash-environments
- Hide stacktrace on unknown plugin-pype
- Fix linux installation
- Refine dependency installation

## 0.3.0

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

## 0.2.0

- Extended pype.config.system-info
- Alternative shell command (instead of `pype`) configurable via config file entry `core_config.shell_command`
- Normalization of command names
- Add flake8-blind-except linter
- Make keyboard interrupt silent on subprocess
- Internal class renaming for consistency

## 0.1.2

- Add <https://pypi.org/project/progress/> as external dependency
- Refine `pype --list`
- Add `pype pype.config system-info`
- Add `make profile` to benchmark runtime performance
- Fix docker image for mint-installation testing

## 0.1.1

- Fixed missing jsonschema dependency in setup.py

## 0.1.0

- Stabilized interfaces
- Added configuration file schema validation using jsonschema
- Support extended to Python >=3.5
- Extended linter configuration
