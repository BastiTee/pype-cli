# Changelog

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
