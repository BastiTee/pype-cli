#!/bin/sh
set -e  # Always exit on non-zero return codes
cd "$( cd "$( dirname "$0" )"; pwd )"

# Check python and pipenv installation
[ -z "$( command -v python3 )" ] && { echo "python3 not available."; exit 1; }
[ -z "$( command -v pipenv )" ] && { echo "pipenv not available."; exit 1; }

# Allow to customize this script with a make-extension file
[ -f "make-extension" ] && . ./make-extension

# Suppress warning if pipenv is started inside .venv
export PIPENV_VERBOSITY=${PIPENV_VERBOSITY:--1}
# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT=${PIPENV_VENV_IN_PROJECT:-1}
# Setup python path
export PYTHONPATH=${PYTHONPATH:-.}
# Setup modules used for linting
export LINTED_MODULES=${LINTED_MODULES:-pype}
# Make sure we are running with an explicit encoding
export LC_ALL=${PYPE_ENCODING:-${LC_ALL}}
export LANG=${PYPE_ENCODING:--${LANG}}
# Default pype configuration file (always use the one relative to make file)
export PYPE_CONFIGURATION_FILE="$( pwd )/config.json"

venv() {
    # Create a pipenv virtual environment for IDE/coding support
    rm -rf .venv
	pipenv install --dev --skip-lock
    pipenv run pip install --editable .
}

clean() {
    # Clean project base by deleting any non-VC files
    rm -rf .venv build dist .pytest_cache *.egg-info
}

test() {
    # Run all tests in default virtualenv
    pipenv run py.test $@
}

coverage() {
    # Run test coverage checks
    pipenv run py.test -c .coveragerc --verbose tests
}

lint() {
    # Run linter / code formatting checks against source code base
    pipenv run flake8 $LINTED_MODULES tests
}

install_pype_core() {
    # Installs main component from source
    if [ -d pype ]; then
        # If inside pype project
        python3 -m pip install --user --force --editable .
    else
        # If pype is embedded as library
        python3 -m pip install --user --editable ./lib/pype
    fi
}

uninstall() {
    # Uninstall pype from global system
    echo "-- Uninstall shell support"
    pype pype.config shell-uninstall 2>/dev/null ||true
    echo "-- Uninstall python librarires"
    python3 -m pip uninstall -y pype-cli3
}

install() {
    # Install pype to global system
    uninstall ||true
    install_pype_core
    pype pype.config shell-install
}

# -----------------------------------------------------------------------------
internal_print_commands() {
    echo "$1\n"
    {   # All functions in make or make-extension are considered targets
        cat make 2>/dev/null
        cat make-extension 2>/dev/null
    } | egrep -e "^[a-zA-Z_]+\(\)" | egrep -ve "^internal" |\
    tr "(" " " | awk '{print $1}' | sort
    echo
}
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    internal_print_commands "Available:"
    exit 0
fi
if [ $# = 0 ]; then
    internal_print_commands "No command selected. Available:"
    exit 1
fi
# Execute the provided command line
$@
