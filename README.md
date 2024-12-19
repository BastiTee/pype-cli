# pype-cli

> ![pype-cli Logo](res/icon-64.png) **A command-line tool for command-line tools**

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/BastiTee/pype-cli/build.yml?branch=main) ![PyPU - Version](https://img.shields.io/pypi/v/pype-cli.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pype-cli.svg)

## In a nutshell

**pype-cli** is a command-line tool to manage sets of other command-line tools. It simplifies the creation, orchestration and access of Python scripts that you require for your development work, process automation, etc.

![pype-cli GIF](res/pype-cli.gif)

## Quickstart

- Install **pype-cli** via `python -m pip install --user pype-cli`. This will install the command `pype` for the current user
- To use an alternative name you need to install from source via `PYPE_CUSTOM_SHELL_COMMAND=my_cmd_name python setup.py install --user`
- Run `pype pype.config shell-install` and open a new shell to activate shell completion
- Create a new **plugin** in your home folder: `pype pype.config plugin-register --create --name my-plugin --path ~/`
- Create a sample **pype** for your plugin: `pype my-plugin --create-pype my-pype`
- Run your **pype**: `pype my-plugin my-pype`
- Show and edit the template **pype** you've just created: `pype my-plugin --open-pype my-pype`

You'll find more information on the commands in the sections below.

## Usage

**pype-cli** builds upon **plugins** and **pypes**. A **pype** is a single Python script whereas a **plugin** is essentially a Python module that extens **pype-cli** with a collection of **pypes**.

**pype-cli** ships with one built-in **plugin** called `pype.config` that is used to configure **pype-cli**. All of the required information will be stored to a local JSON-configuration file that defaults to `~/.pype-cli/config.json`. To configure a custom configuration folder use the environment variable `PYPE_CONFIG_FOLDER`. For example to use `/path/to/pype-cli/config.json` as configuration folder/file put into your `~/.bashrc` file: `export PYPE_CONFIG_FOLDER=/path/to/pype-cli`.

### Basic operations

- List all available **pypes**: `pype --list-pypes`
- Open **pype-cli**'s configuration file: `pype --open-config`
- Refer to `pype ... --help` for further information on the command-line

For all options you will find a short variant such as `-h` for `--help` or `pype -l` instead of `pype --list-pypes`. They are omitted here for better readability.

### Install pype autocompletion and aliases

**pype-cli**'s main benefit is that is is extendable with custom **plugins** and that it will allow you to immediatelly browse and use newly created and existing **plugins**/**pypes** by using the `<TAB>` key and by configuring short **aliases**. To enable the functionality it is required to install a source-script to your shell's rc-file that will be executed everytime you open a shell.

- Run `pype pype.config shell-install`
- Run `pype pype.config shell-uninstall` to remove if necessary

If you want to use one-tab completion (instead of two tab presses) you can add the following section to your `.bashrc` file:

```shell
bind 'set show-all-if-ambiguous on'
bind 'set completion-ignore-case on'
```

For `.zshrc` apply instead:

```shell
unsetopt listambiguous
```

### Un-/register plugins

- Register an existing **plugin**: `pype pype.config plugin-register --name myplugin --path ~/pype_plugins` (`myplugin` is a Python module with at least an `__init__.py` file and `~/pype_plugins` a folder where the **plugin** is stored)
- On-the-fly create and register a new **plugin**: `pype pype.config plugin-register --create --name myplugin --path ~/pype_plugins`
- Unregister (but not delete) a **plugin**: `pype pype.config plugin-unregister --name myplugin`

### Create, open and delete pypes

To create a new pype you need to decide to which plugin you want to add the pype, e.g., `myplugin`.

- Create a new **pype** from a template: `pype myplugin --create mypype`
- Create a new **pype** from a template with less boilerplate: `pype myplugin --minimal --create mypype`
- Create a new **pype** from minimal template and open immediately: `pype myplugin --minimal --edit --create mypype`
- Open a **pype** in your default editor: `pype myplugin --open-pype mypype`
- Delete a **pype**: `pype myplugin --delete-pype mypype`

### Un-/register aliases

If you have selected a **pype** from a **plugin** you can set **aliases** for it. Afterwards you need to start a new shell session or source your rc-file to activate the **aliases**. New **aliases** are stored in the configuration file.

- Register an **alias**: `pype --alias-register mm myplugin mypype` → `alias mm="pype myplugin mypype"`
- Register an **alias with options**: `pype --alias-register mm myplugin mypype --option opt1 --toggle` → `alias mm="pype myplugin mypype --option opt1 --toggle"`
- Unregister an **alias**: `pype --alias-unregister mm`
- List all avaliable **aliases**: `pype --aliases`

### Global logging configuration

**pype-cli** contains a built-in file logger setup. To configure it use the **pype** `pype pype.config logger`. In your **pypes** you can use it right away like this:

```python
import logging
import click

@click.command(name='my-pype', help=__doc__)
def main() -> None:
    # Name your logger. Note that this can be omitted but you will end up
    # with the default 'root' logger.
    logger = logging.getLogger(__name__)

    # Log something to the global log file. Note that the output to the file
    # depends on the logging configuration mentioned above.
    logger.debug('Debug message')
    logger.info('Info message')
```

- Enable/disable global logging: `pype pype.config logger enable/disable`
- Print current configuration: `pype pype.config logger print-config`
- Set logging folder: `pype pype.config logger set-directory /your/login/folder`
- Set logging level: `pype pype.config logger set-level DEBUG`
- Set logging pattern: `pype pype.config logger set-pattern "%(asctime)s %(levelname)s %(name)s %(message)s"`

### Shared code for plugins

If your **plugin** contains shared code over all **pypes** you can simply put it into a subpackage of your **plugin** or into a file prefixed with `__`, e.g., `__commons__.py`. **pype-cli** will only scan / consider top-level Python scripts without underscores as **pypes**.

### Best practises

**pype-cli** has been built around the [Click-project ("Command Line Interface Creation Kit")](https://click.palletsprojects.com/) which is a Python package for creating beautiful command line interfaces. To fully utilize the capabilities of **pype-cli** it is highly recommended to get familiar with the project and use it in your **pypes** as well.

## pype-cli development

- Run `make venv` to create a new virtual environment
- Run `pipenv shell` to activate a local shell with the required configurations
- Run `pype` to operate locale development version (it will react to code changes)
- Run `PYPE_BENCHMARK_INIT=1 pype` to print loading times for individual plugins or pypes

### How to release

- Switch to latest `main` branch after making sure [it is stable](https://github.com/BastiTee/pype-cli/actions)
- Get latest changelog via `make changelog` and update `CHANGELOG.md`
- Run `NEXT_VERSION=0.0.3 make release`
- Trigger [Github action](https://github.com/BastiTee/pype-cli/actions?query=workflow%3ARelease) to release to PyPi

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).

Icon made by [Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/free-icon/pipeline_1432915) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).
