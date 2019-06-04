#!/bin/sh
cd "$( cd "$( dirname "$0" )"; pwd )"

export PIPENV_VERBOSITY=-1  # suppress warning if pipenv is started inside venv
export PIPENV_VENV_IN_PROJECT=1  # use relative .venv folder
export PYTHONPATH=.  # include source code in any python subprocess
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYPE_CONFIGURATION_FILE="$( pwd )/config.json"

shell() {
    # Initialize virtualenv, i.e., install required packages etc.
    echo " === SHELL === "
    if [ -z "$( command -v python3 )" ]; then
        echo "python3 not available."
        exit 1
    fi
    # Since it's not very expensive we recreate the venv everytime
    rm -rf .venv
    # Install basic venv and pype codebase
    python3 -m pip install pipenv --upgrade
	pipenv install --dev --skip-lock ||exit 1
    # Configure shell to use custom config
    # echo "export PYPE_CONFIGURATION_FILE=\"$( pwd )/config.json\"" \
    # >> ".venv/bin/activate"
    # Install and configure pype
    pipenv run pip install --editable .
    pipenv run pype pype.config install-shell -t ".venv/bin/activate"
    # Spawn a venv shell
    pipenv shell
}

clean() {
    # Clean project base by deleting any non-VC files
    echo " === CLEAN === "
    rm -fr build dist .egg *.egg-info
}

test() {
    # Run all tests in default virtualenv
    echo " === TEST === "
    pipenv run py.test $@ ||exit 1
}

testall() {
    # Run all tests against all virtualenvs defined in tox.ini
    echo " === TESTALL === "
    pipenv run detox $@ ||exit 1
}

coverage() {
    # Run test coverage checks
    echo " === COVERAGE === "
    pipenv run py.test -c .coveragerc --verbose tests $@ ||exit 1
}

lint() {
    # Run linter / code formatting checks against source code base
    echo " === LINT === "
    pipenv run flake8 pype tests $@  ||exit 1
}

profile() {
    # Run a profiler to analyse the runtime
    pipenv run python -m profile -o tests/profile.obj pype/__main__.py \
    >/dev/null
    pipenv run python tests/run_pstats.py
}

package() {
    # Run package setup
    echo " === PACKAGE === "
    pipenv run python setup.py bdist_wheel $@
}

build() {
    # Run setup.py-based build process to package application
    echo " === BUILD === "
    test
    coverage
    lint
    package
}

publish() {
    # Publish pype to pypi.org
    echo " === PUBLISH === "
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
    echo " === INSTALL === "
    build
    python3 -m pip install dist/*.whl
}

dockerize() {
    # Install pype into a dockercontainer to test mint-installation
    echo " === DOCKERIZE === "
    clean
    build
    docker build -t "pype-docker" .
    docker run --rm -ti "pype-docker"
}

changelog() {
    # Return changelog since last version tag
    echo " === CHANGELOG === "
    last_version=$( git tag | sort --version-sort -r | head -n1 )
    version_hash=$( git show-ref -s $last_version )
    echo "--- $last_version $version_hash"
    git log --pretty=format:"%s" $version_hash..HEAD
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
