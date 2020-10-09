# pype-cli

> A command-line tool for command-line tools
<img align="right" src="res/icon.png" alt="pype-cli Logo" width="150" height="150">

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/BastiTee/pype-cli/CI)
![PyPU - Version](https://img.shields.io/pypi/v/pype-cli.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pype-cli.svg)

## In a nutshell

__pype-cli__ is a command-line tool to manage sets of other command-line tools. It simplifies the creation, orchestration and access of Python scripts that you require for your development work, process automation, etc.

<img src="res/pype-cli.gif" alt="pype-cli GIF" width="550">

## Quickstart

* Install __pype-cli__ via `pip3 install --user pype-cli`. This will install the command `pype` for the current user
* To use an alternative name you need to install from source via `PYPE_CUSTOM_SHELL_COMMAND=my_cmd_name python3 setup.py install --user`
* Run `pype pype.config shell-install` and open a new shell to activate shell completion
* Create a new __plugin__ in your home folder: `pype pype.config plugin-register --create --name my-plugin --path ~/`
* Create a sample __pype__ for your plugin: `pype my-plugin --create-pype my-pype`
* Run your __pype__: `pype my-plugin my-pype`
* Show and edit the template __pype__ you've just created: `pype my-plugin --open-pype my-pype`

You'll find more information on the commands in the sections below.

## Usage

__pype-cli__ builds upon __plugins__ and __pypes__. A __pype__ is a single Python script whereas a __plugin__ is essentially a Python module that extens __pype-cli__ with a collection of __pypes__.

__pype-cli__ ships with one built-in __plugin__ called `pype.config` that is used to configure __pype-cli__. All of the required information will be stored to a local JSON-configuration file that defaults to `~/.pype-cli/config.json`. To configure a custom configuration folder use the environment variable `PYPE_CONFIG_FOLDER`. For example to use `/path/to/pype-cli/config.json` as configuration folder/file put into your `~/.bashrc` file: `export PYPE_CONFIG_FOLDER=/path/to/pype-cli`.

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

* Register an __alias__: `pype --alias-register mm myplugin mypype` → `alias mm="pype myplugin mypype"`
* Register an __alias with options__: `pype --alias-register mm myplugin mypype --option opt1 --toggle` → `alias mm="pype myplugin mypype --option opt1 --toggle"`
* Unregister an __alias__: `pype --alias-unregister mm`
* List all avaliable __aliases__: `pype --aliases`

### Global logging configuration

__pype-cli__ contains a built-in logger setup. To configure it use the __pype__ `pype pype.config logger`. In your __pypes__ you can use it right away [like in the provided example](example_pypes/basics/logger.py).

* Enable/disable global logging: `pype pype.config logger enable/disable`
* Print current configuration: `pype pype.config logger print-config`
* Set logging folder: `pype pype.config logger set-directory /your/login/folder`
* Set logging level: `pype pype.config logger set-level DEBUG`
* Set logging pattern: `pype pype.config logger set-pattern "%(asctime)s %(levelname)s %(name)s %(message)s"`

### Shared code for plugins

If your __plugin__ contains shared code over all __pypes__ you can simply put it into a subpackage of your __plugin__ or into a file prefixed with `__`, e.g., `__commons__.py`. __pype-cli__ will only scan / consider top-level Python scripts without underscores as __pypes__.

### Example recipes

You can register a sample __plugin__ called [__basics__](example_pypes/basics) that contains some useful recipes to get you started with your own pipes.

* Register the [__basics__](example_pypes/basics) __plugin__: `pype pype.config plugin-register --name basics --path <PYPE_REPOSITORY>/example_pypes`
* Navigate to `pype basics <TAB>` to see its content
* Open a recipe in your edior, for example: `pype basics --open-pype hello-world-opt`

For some basic information you can also refer to the built-in [template.py](pype/template.py) and [template_minimal.py](pype/template_minimal.py) that are used on creation of new __pypes__.

Note that as long as you don't import some of the [convenience utilities](pype/__init__.py) of __pype-cli__ directly, your __pype__ will remain [an independent Python script](example_pypes/basics/non_pype_script.py) that can be used regardless of __pype_cli__.

### Best practises

__pype-cli__ has been built around the [Click-project ("Command Line Interface Creation Kit")](https://click.palletsprojects.com/) which is a Python package for creating beautiful command line interfaces.
To fully utilize the capabilities of __pype-cli__ it is highly recommended to get familiar with the project and use it in your __pypes__ as well.
Again you can refer to the [__basics__](example_pypes/basics) plugin for guidance.

## pype-cli development

* Run `make venv` to create a new virtual environment
* Run `pipenv shell` to activate a local shell with the required configurations
* Run `pype` to operate locale development version (it will react to code changes)
* Run `PYPE_BENCHMARK_INIT=1 pype` to print loading times for individual plugins or pypes

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).

Icon made by [Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/free-icon/pipeline_1432915) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).
