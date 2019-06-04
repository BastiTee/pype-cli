# Changelog

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
