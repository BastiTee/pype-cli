#!/bin/sh
set -e  # Always exit on non-zero return codes
cd "$( cd "$( dirname "$0" )"; pwd )"

# Check python and pipenv installation
[ -z "$( command -v python3 )" ] && { echo "python3 not available."; exit 1; }
[ -z "$( command -v pipenv )" ] && { echo "pipenv not available."; exit 1; }

# Suppress warning if pipenv is started inside .venv
export PIPENV_VERBOSITY=${PIPENV_VERBOSITY:--1}
# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT=${PIPENV_VENV_IN_PROJECT:-1}
# Ignore existing venvs (required for travis)
export PIPENV_IGNORE_VIRTUALENVS=${PIPENV_IGNORE_VIRTUALENVS:-1}
# Setup python path
export PYTHONPATH=${PYTHONPATH:-.}
# Make sure we are running with an explicit encoding
export LC_ALL=${PYPE_ENCODING:-${LC_ALL}}
export LANG=${PYPE_ENCODING:--${LANG}}
# Default pype configuration file (always use the one relative to make file)
export PYPE_CONFIG_FOLDER="$( pwd )/.pype-cli"

venv() {
    # Create a pipenv virtual environment for IDE/coding support
    rm -rf .venv $PYPE_CONFIG_FOLDER
	pipenv install --dev --skip-lock
    pipenv run pip install --editable .
    # Use a venv-relative config file
    mkdir -p $PYPE_CONFIG_FOLDER
    echo "export PYPE_CONFIG_FOLDER=$PYPE_CONFIG_FOLDER" >> .venv/bin/activate
    # Auto-activate shell completion
    echo "eval \"\$(_PYPE_COMPLETE=source pype)\"" >> .venv/bin/activate
    # Register example pype
    pipenv run pype pype.config plugin-register \
    --name basics --path example_pypes
}

clean() {
    # Clean project base by deleting any non-VC files
    rm -rf .venv build dist .pytest_cache *.egg-info .pype-cli*
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
    pipenv run flake8 pype example_pypes tests
}

package() {
    # Run package setup
    pipenv run python setup.py bdist_wheel $@
}

build() {
    # Run setup.py-based build process to package application
    clean
    venv
    test
    coverage
    lint
    package
}

publish() {
    # Publish pype to pypi.org
    branch=$( git rev-parse --abbrev-ref HEAD )
    if [ $branch != "master" ]; then
        echo "Only publish released master branches! Currently on $branch"
        exit 1
    fi
    build
    pipenv run twine upload dist/*
}

dockerize() {
    # Install pype into a dockercontainer to test mint-installation
    build
    image_name="pype-docker-mint-install"
    docker build -t $image_name .
    docker run -ti --rm $image_name $@
}

changelog() {
    # Return changelog since last version tag
    last_version=$( git tag | sort --version-sort -r | head -n1 )
    version_hash=$( git show-ref -s $last_version )
    echo "--- $last_version $version_hash"
    git log --pretty=format:"- %s" $version_hash..HEAD
}

# -----------------------------------------------------------------------------
internal_print_commands() {
    echo "$1\n"
    {   # All functions except prefixed "internal_"  are considered targets
        cat make 2>/dev/null
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
