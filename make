#!/bin/sh
set -e  # Always exit on non-zero return codes
cd "$( cd "$( dirname "$0" )"; pwd )"

# Check python and pipenv installation
[ -z "$( command -v python3 )" ] && { echo "python3 not available."; exit 1; }
[ -z "$( command -v pipenv )" ] && python3 -m pip install pipenv --upgrade

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
# Make sure we are running UTF-8 encoding
export LC_ALL=${LC_ENCODING:-C.UTF-8}
export LANG=${LC_ENCODING:-C.UTF-8}
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
    git status --ignored --short |grep -e "^!!" |awk '{print $2}' |\
    while read file; do rm -vfr $file; done
}

test() {
    # Run all tests in default virtualenv
    pipenv run py.test
}

coverage() {
    # Run test coverage checks
    pipenv run py.test -c .coveragerc --verbose tests
}

lint() {
    # Run linter / code formatting checks against source code base
    pipenv run flake8 $LINTED_MODULES tests
}

install_deps_globally() {
    # Install to global python installation all required dependencies
    pipenv lock -r > requirements.txt
    python3 -m pip install -r requirements.txt
}

uninstall() {
    # Uninstall pype from global system
    echo "-- Uninstall shell support"
    pype pype.config shell-uninstall 2>/dev/null
    echo "-- Uninstall python librarires"
    python3 -m pip uninstall -y pype-cli
}

install() {
    # Install pype to global system
    uninstall ||true
    install_deps_globally
    if [ -d pype ]; then
        # If inside pype project
        python3 -m pip install --editable . 2>/dev/null
    else
        # If pype is embedded as library
        python3 -m pip install --editable ./lib/pype 2>/dev/null
    fi
    pype pype.config shell-install
}

# -----------------------------------------------------------------------------
function print_commands() {
    echo "$1\n"
    {   # All functions in make or make-extension are considered targets
        cat make 2>/dev/null
        cat make-extension 2>/dev/null
    } | egrep -e "^[a-zA-Z_]+\(\)" | tr "(" " " | awk '{print $1}' | sort
    echo
}
if [ $# == 0 ]; then
    print_commands "No command selected. Available:"
    exit 1
fi
# Execute the provided command line
$@ ||print_commands "Unknown command. Available:"
