#!/bin/sh
cd "$( cd "$( dirname "$0" )"; pwd )"

TARGET_PORT=9690
PROJECT_NAME="pype"

export PIPENV_VERBOSITY=-1  # suppress warning if pipenv is started inside venv
export PYTHONPATH=.  # include source code in any python subprocess
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

init() {
    # Initialize virtualenv, i.e., install required packages etc.
    if [ -z "$( command -v python3 )" ]; then
        echo "python3 not available."
        exit 1
    fi
    python3 -m pip install pipenv --upgrade
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --skip-lock
}

shell() {
    # Initialize virtualenv and open a new shell using it
    init
    pipenv shell
}

clean() {
    # Clean project base by deleting any non-VC files
	git clean -fdx
}

test() {
    # Run all tests in default virtualenv
    pipenv run py.test $@
}

testall() {
    # Run all tests against all virtualenvs defined in tox.ini
    pipenv run detox $@
}

coverage() {
    # Run test coverage checks
    pipenv run py.test -c .coveragerc --verbose tests $@
}

lint() {
    # Run linter / code formatting checks against source code base
    pipenv run flake8 $PROJECT_NAME $@
}

build() {
    # Run setup.py-based build process to package application
    rm -fr build dist .egg *.egg-info
    pipenv run python setup.py bdist_wheel $@
}

publish() {
    sudo -H pip install 'twine>=1.5.0'
    build && twine upload dist/*
}

commit() {
    # Run full build toolchain before executing a git commit
    all && git commit
}

all() {
    # Full build toolchain
    init && test && lint && coverage && build
}

# -----------------------------------------------------------------------------

coms=$( cat $0 | egrep "\(\) {" |tr "(" " " |awk '{print $1}' |tr "\n" " " )
if [ -z "$1" ]; then
    echo "Select command: $coms"
    exit 1
fi
if [ -z "$( echo $coms | grep $1 )" ]; then
    echo "Unknown command. options: $coms"
    exit 1
fi
command=$1
shift
$command $@
