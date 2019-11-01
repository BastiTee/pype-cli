# pype

> A command-line tool for command-line tools
<img align="right" src="res/icon.png" alt="pype-cli Logo" width="150" height="150">

[![Build Status](https://travis-ci.org/BastiTee/pype-cli.svg?branch=develop)](https://travis-ci.org/BastiTee/pype-cli)
![PyPU - Version](https://img.shields.io/pypi/v/pype-cli.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pype-cli.svg)

## In a nutshell

__pype-cli__ is a command-line tool to manage sets of other command-line tools. It simplifies the creation, orchestration and access of Python scripts that you require for your development work, process automation, etc.

<img src="res/terminalizer/pype-cli.gif" alt="pype-cli GIF" width="550">

## Quickstart

* Install __pype-cli__ via `pip3 install --user pype-cli`. This will install the command `pype` on your system
* To use an alternative name you need to install from source via `PYPE_CUSTOM_SHELL_COMMAND=my_cmd_name python3 setup.py install --user`
* Run `pype pype.config shell-install` and open a new shell to activate shell completion
* Create a new __plugin__ in your home folder: `pype pype.config plugin-register --create --name my-plugin --path ~/`
* Create a sample __pype__ for your plugin: `pype my-plugin --create-pype my-pype`
* Run your __pype__: `pype my-plugin my-pype`
* Show and edit the template __pype__ you've just created: `pype my-plugin --open-pype my-pype`

You'll find more information on the commands in the sections below.

## Usage

__pype-cli__ builds upon __plugins__ and __pypes__. A __pype__ is a single Python script whereas a __plugin__ is essentially a Python module that extens __pype-cli__ with a collection of __pypes__.

__pype-cli__ ships with one built-in __plugin__ called `pype.config` that is used to configure __pype-cli__. All of the required information will be stored to a local JSON-configuration file that defaults to `~/.pype-config.json`. To configure a custom configuration file use the environment variable `PYPE_CONFIGURATION_FILE`, e.g. in your `~/.bashrc` file set `export PYPE_CONFIGURATION_FILE=/path/to/myconfig.json`.

### Basic operations

* List all available __pypes__: `pype --list-pypes`
* Open __pype-cli__'s configuration file: `pype --open-config`
* Refer to `pype ... --help` for further information on the command-line

For all options you will find a short variant such as `-h` for `--help` or `pype -l` instead of `pype --list-pypes`. They are omitted here for better readability.

### Install pype autocompletion and aliases

__pype-cli__'s main benefit is that is is extendable with custom __plugins__ and that it will allow you to immediatelly browse and use newly created and existing __plugins__/__pypes__ by using the `<TAB>` key and by configuring short __aliases__. To enable the functionality it is required to install a source-script to your shell's rc-file that will be executed everytime you open a shell.

* Run `pype pype.config shell-install`
* Run `pype pype.config shell-uninstall` to remove if necessary

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

* Register an existing __plugin__: `pype pype.config plugin-register --name myplugin --path ~/pype_plugins` (`myplugin` is a Python module with at least an `__init__.py` file and `~/pype_plugins` a folder where the __plugin__ is stored)
* On-the-fly create and register a new __plugin__: `pype pype.config plugin-register --create --name myplugin --path ~/pype_plugins`
* Unregister (but not delete) a __plugin__: `pype pype.config plugin-unregister --name myplugin`

### Create, open and delete pypes

To create a new pype you need to decide to which plugin you want to add the pype, e.g., `myplugin`.

* Create a new __pype__ from a template: `pype myplugin --create mypype`
* Create a new __pype__ from a template with less boilerplate: `pype myplugin --minimal --create mypype`
* Create a new __pype__ from minimal template and open immediately: `pype myplugin --minimal --edit --create mypype`
* Open a __pype__ in your default editor: `pype myplugin --open-pype mypype`
* Delete a __pype__: `pype myplugin --delete-pype mypype`

### Un-/register aliases

If you have selected a __pype__ from a __plugin__ you can set __aliases__ for it. Afterwards you need to start a new shell session or source your rc-file to activate the __aliases__. New __aliases__ are stored in the configuration file.

* Register an __alias__: `pype --register-alias mm myplugin mypype` → `alias mm="pype myplugin mypype"`
* Register an __alias with options__: `pype --register-alias mm myplugin mypype --option opt1 --toggle` → `alias mm="pype myplugin mypype --option opt1 --toggle"`
* Unregister an __alias__: `pype --unregister-alias mm`

### Shared code for plugins

If your __plugin__ contains shared code over all __pypes__ you can simply put it into a subpackage of your __plugin__ or into a file prefixed with `__`, e.g., `__commons__.py`. __pype-cli__ will only scan / consider top-level Python scripts without underscores as __pypes__.

### Example recipes

You can register a sample __plugin__ called [__basics__](example_pypes/basics) that contains some useful recipes to get you started with your own pipes.

* Register the [__basics__](example_pypes/basics) __plugin__: `pype pype.config plugin-register --name basics --path <PYPE_REPOSITORY>/example_pypes`
* Navigate to `pype basics <TAB>` to see its content
* Open a recipe in your edior, for example: `pype basics --open-pype hello-world-opt`

For some basic information you can also refer to the built-in [template.py](pype/template.py) and [template_minimal.py](pype/template_minimal.py) that are used on creation of new __pypes__.

## Development

* Run `./make venv` to create a new virtual environment
* Run `pipenv shell` to activate a local shell with the required configurations
* Run `pype` to operate locale development version (it will react to code changes)

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).

Icon made by [Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/free-icon/pipeline_1432915) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).
