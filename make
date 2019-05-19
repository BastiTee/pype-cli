#!/bin/sh
cd "$( cd "$( dirname "$0" )"; pwd )"

PROJECT_NAME="pype"
export PIPENV_VERBOSITY=-1  # suppress warning if pipenv is started inside venv
export PIPENV_VENV_IN_PROJECT=1  # use relative .venv folder
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
	pipenv install --dev --skip-lock
    # Install bash completion
    echo "eval \"\$(_PYPE_COMPLETE=source pype)\"" >> .venv/bin/activate
}

shell() {
    # Initialize virtualenv and open a new shell using it
    if [ ! -d ".venv" ]; then
        ./make init
    fi
    pipenv run pip install --editable .
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
    test
    coverage
    lint
    pipenv run python setup.py bdist_wheel $@
}

publish() {
    branch=$( git rev-parse --abbrev-ref HEAD )
    if [ $branch != "master" ]; then
        echo "Only publish released master branches! Currently on $branch"
        exit 1
    fi
    build
    pipenv run twine upload dist/*
}

install() {
    # Install pype globally on host system
    build
    python3 -m pip install dist/*.whl
}

dockerize() {
    # Install pype into a dockercontainer to test mint-installation
    build
    docker build -t $PROJECT_NAME .
    docker run --rm -ti $PROJECT_NAME
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
