# pype
> A command-line tool for command-line tools
<img align="right" src="res/icon.png" alt="alt text" width="150" height="150">

## Installation

Install using `python3 -m pip install pype-cli` or `pip3 install pype-cli`

## Usage

__pype-cli__ builds upon __plugins__ and __pypes__. A __pype__ is a single Python script whereas a __plugin__ is basically a Python module that extens __pype-cli__ with a collection of __pypes__.
__pype-cli__ ships with one built-in __plugin__ called `pype.config` that is used to configure __pype-cli__. All of the required information will be stored to a local configuration file.

* List all available __pypes__: `pype -l`
* Open __pype-cli__'s configuration file: `pype -o`

To configure a custom configuration file use the environment variable `PYPE_CONFIGURATION_FILE`, e.g. in your `~/.bashrc` file set `export PYPE_CONFIGURATION_FILE=/path/to/myconfig.json`. If not set a default configuration file will be created at `~/.pype-config.json`.

### Install pype autocompletion and aliases

* Run `pype pype.config install-shell -t ~/.bashrc` for bash shells
* Run `pype pype.config install-shell -t ~/.zshrc` for zsh shells

### Un-/register plugins

* Register an existing __plugin__: `pype pype.config plugin-register -n myplugin -p ~/pype_plugins`
* Create and register a new __plugin__: `pype pype.config plugin-register -c -n myplugin -p ~/pype_plugins`
* Unregister a __plugin__: `pype pype.config plugin-unregister -n myplugin`

### Create, open and delete pypes

To create a new pype you need to decide to which plugin you want to add the pype, e.g., myplugin.

* Create a new __pype__: `pype myplugin -c mypype`
* Open a __pype__ in your default editor: `pype myplugin -o mypype`
* Delete a __pype__: `pype myplugin -d mypype`

### Un-/register pype aliases

If you have selected a __pype__ from a __plugin__ you can set __aliases__ for it. Afterwards you need to start a new shell session to activate the __aliases__. They will be stored to your configuration file as well.

* Register an __alias__: `pype -r mm myplugin mypype` → `alias mm="pype myplugin mypype"`
* Register an __alias with options__: `pype -r mm myplugin mypype -o opt1 -v` → `alias mm="pype myplugin mypype -o opt1 -v"`
* Unregister an __alias__: `pype -u mm`

## Development

* Run `./make shell` to open a `pipenv` shell with the required shell configuration
* Run __pype__ to operate locale development version (it will react to code changes)

## To-Do's

This project is currently a proof of concept.

* [ ] Validate config.json before using it (see <https://pypi.org/project/jsonschema/>)
* [x] Allow aliasing of pype calls
* [x] Allow creating plugins on the fly
* [x] Add coloring library
* [x] Extend documentation of template pype
* [x] Add help texts to commands
* [x] Auto-install bash/zsh completion
* [x] Find another name since pype is unavailable in PyPi `¯\_(ツ)_/¯`
* [x] Improve config file resolving to envvar->homefile->currdir->default
* [x] Add option to add/delete plugins via pype
* [x] Add option to create a new pype via pype
* [x] Add option to open a pype in default browser
* [x] Internalize default pypes such as 'version'
* [x] Create a docker image to test installation on a mint system
* [x] Auto-complete custom pypes using Click
* [x] Allow separation of subcommand options and pype-internal options (e.g. `-h` option)
* [x] Move example pypes to dedicated folder and make path configurable
* [x] Find a way to re-use module and script documentation for CLI documentation
* [x] Introduce verbosity option
* [x] Introduce a logging framework
* [x] Add auto-listing of configured pypes
* [x] Allow configuring custom pypes via configuration file
* [x] Introduce configuration file
* [x] Check how to backward-support shell scripts
* [x] Setup with python3 best-practices boilerplate

## Important resources

* <https://click.palletsprojects.com/en/7.x/>
* <http://click.palletsprojects.com/en/7.x/commands/>
* <https://click.palletsprojects.com/en/7.x/bashcomplete/>
* <https://click.palletsprojects.com/en/7.x/api/#click.Context>

## License and attribution

This software is licensed under [Apache License 2.0](LICENSE.txt).

Icon made by [Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/free-icon/pipeline_1432915) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).
