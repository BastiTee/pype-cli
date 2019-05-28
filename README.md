# pype

> A command-line tool for command-line tools
<img align="right" src="res/icon.png" alt="alt text" width="150" height="150">

[![Build Status](https://travis-ci.org/BastiTee/pype.svg?branch=develop)](https://travis-ci.org/BastiTee/pype)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pype-cli.svg)

__Disclaimer: This project is an early POC and interfaces can change anytime.__

## In a nutshell

__pype-cli__ is a CLI-configurable command-line tool to orchestrate sets of other command-line tools. It simplifies the creation, orchestration and access of Python scripts that you require for your development work, process automation, etc.

## Installation

The core package can be installed using `python3 -m pip install pype-cli` or `pip3 install pype-cli`. Refer to the usage section on configuration options.

## Usage

__pype-cli__ builds upon __plugins__ and __pypes__. A __pype__ is a single Python script whereas a __plugin__ is basically a Python module that extens __pype-cli__ with a collection of __pypes__.

__pype-cli__ ships with one built-in __plugin__ called `pype.config` that is used to configure __pype-cli__. All of the required information will be stored to a local JSON-configuration file that defaults to `~/.pype-config.json`. To configure a custom configuration file use the environment variable `PYPE_CONFIGURATION_FILE`, e.g. in your `~/.bashrc` file set `export PYPE_CONFIGURATION_FILE=/path/to/myconfig.json`.

### Basic operations

* List all available __pypes__: `pype -l`
* Open __pype-cli__'s configuration file: `pype -o`
* Refer to `pype ... -h` for further information on the command-line

### Install pype autocompletion and aliases

__pype-cli__'s main benefit is that is is extendable with custom __plugins__ and that it will allow you to immediatelly browse and use newly created and existing __plugins__/__pypes__ by using the `<TAB>` key and by configuring short __aliases__. To enable the functionality it is required to install a source-script to your shell's rc-file that will be executed everytime you open a shell.

* Run `pype pype.config install-shell -t ~/.bashrc` for bash shells
* Run `pype pype.config install-shell -t ~/.zshrc` for zsh shells

### Un-/register plugins

* Register an existing __plugin__: `pype pype.config plugin-register -n myplugin -p ~/pype_plugins` (`myplugin` is a Python module with at least an `__init__.py` file and `~/pype_plugins` a folder where the __plugin__ is stored)
* On-the-fly create and register a new __plugin__: `pype pype.config plugin-register -c -n myplugin -p ~/pype_plugins`
* Unregister (but not delete) a __plugin__: `pype pype.config plugin-unregister -n myplugin`

### Create, open and delete pypes

To create a new pype you need to decide to which plugin you want to add the pype, e.g., `myplugin`.

* Create a new __pype__ from a template: `pype myplugin -c mypype`
* Create a new __pype__ from a template with less boilerplate: `pype myplugin --minimal -c mypype` or `pype myplugin -mc mypype`
* Create a new __pype__ from minimal template and open immediately: `pype myplugin --minimal --edit -c mypype` or `pype myplugin -mec mypype`
* Open a __pype__ in your default editor: `pype myplugin -o mypype`
* Delete a __pype__: `pype myplugin -d mypype`

### Un-/register aliases

If you have selected a __pype__ from a __plugin__ you can set __aliases__ for it. Afterwards you need to start a new shell session or source your rc-file to activate the __aliases__. New __aliases__ are stored in the configuration file.

* Register an __alias__: `pype -r mm myplugin mypype` → `alias mm="pype myplugin mypype"`
* Register an __alias with options__: `pype -r mm myplugin mypype -o opt1 -v` → `alias mm="pype myplugin mypype -o opt1 -v"`
* Unregister an __alias__: `pype -u mm`

### Shared code for plugins

If your __plugin__ contains shared code over all __pypes__ you can simply put it into a subpackage of your __plugin__ or into a file prefixed with `__`, e.g., `__commons__.py`. __pype-cli__ will only scan / consider top-level Python scripts without underscores as __pypes__.

## Development

* Run `./make shell` to open a `pipenv` shell with the required shell configuration
* Run `pype` to operate locale development version (it will react to code changes)

## To-Do's

* ✅️ Validate config.json before using it (see <https://pypi.org/project/jsonschema/>)
* ✅️ Fix pipenv issue on travis CI
* ✅️ Fix travis build for Python 3.5
* ✅️ Fix travis build for Python 3.7
* ✅️ Add free continuous integration
* ✅ Introduce more strict linting, e.g., on scripts using `-` instead of `_` and import order
* ✅ Allow immediate editing of new pypes
* ✅️ Add a template with less boilerplate for advanced users
* ✅ Add a filter to limit plugins to usernames
* ✅ Allow aliasing of pype calls
* ✅ Allow creating plugins on the fly
* ✅ Add coloring library
* ✅ Extend documentation of template pype
* ✅ Add help texts to commands
* ✅ Auto-install bash/zsh completion
* ✅ Find another name since pype is unavailable in PyPi `¯\_(ツ)_/¯`
* ✅ Improve config file resolving to envvar->homefile->currdir->default
* ✅ Add option to add/delete plugins via pype
* ✅ Add option to create a new pype via pype
* ✅ Add option to open a pype in default browser
* ✅ Internalize default pypes such as 'version'
* ✅ Create a docker image to test installation on a mint system
* ✅ Auto-complete custom pypes using Click
* ✅ Allow separation of subcommand options and pype-internal options (e.g. `-h` option)
* ✅ Move example pypes to dedicated folder and make path configurable
* ✅ Find a way to re-use module and script documentation for CLI documentation
* ✅ Introduce verbosity option
* ✅ Introduce a logging framework
* ✅ Add auto-listing of configured pypes
* ✅ Allow configuring custom pypes via configuration file
* ✅ Introduce configuration file
* ✅ Check how to backward-support shell scripts
* ✅ Setup with python3 best-practices boilerplate

## Important resources

* <https://click.palletsprojects.com/en/7.x/>
* <http://click.palletsprojects.com/en/7.x/commands/>
* <https://click.palletsprojects.com/en/7.x/bashcomplete/>
* <https://click.palletsprojects.com/en/7.x/api/#click.Context>

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).

Icon made by [Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/free-icon/pipeline_1432915) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).
