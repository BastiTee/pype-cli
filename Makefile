# Required executables
ifeq (, $(shell which python3))
 $(error "No python3 on PATH.")
endif
ifeq (, $(shell which pipenv))
 $(error "No pipenv on PATH.")
endif

# Suppress warning if pipenv is started inside .venv
export PIPENV_VERBOSITY=1
# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT=1
# Ignore existing venvs (required for travis)
export PIPENV_IGNORE_VIRTUALENVS=1
# Make sure we are running with an explicit encoding
export LC_ALL=C
export LANG=C.UTF-8

all: prepare build

prepare: clean
	@echo Preparing virtual environment
	pipenv install --dev

build: test coverage isort lint
	@echo Run setup.py-based build process to package application
	pipenv run python setup.py bdist_wheel

shell:
	@echo Initialize virtualenv and open a new shell using it
	pipenv shell

clean:
	@echo Clean project base
	rm -rf .venv build dist .pytest_cache *.egg-info src Pipfile.lock

test:
	@echo Run all tests in default virtualenv
	pipenv run py.test tests

testall:
	@echo Run all tests against all virtualenvs defined in tox.ini
	pipenv run tox -c setup.cfg tests

coverage:
	@echo Run test coverage checks
	pipenv run py.test --verbose tests

isort:
	@echo Check for incorrectly sorted imports
	pipenv run isort --check-only pype tests example_pypes

isort-apply:
	@echo Check for incorrectly sorted imports
	pipenv run isort pype tests example_pypes

lint:
	@echo Run code formatting checks against source code base
	pipenv run flake8 pype tests example_pypes

dockerize: build
	@echo Install pype into a dockercontainer to test mint installation
	docker build -t "pype-docker-mint-install" .
	docker run -ti --rm "pype-docker-mint-install"

publish:
	@echo Publish pype to pypi.org
	pipenv run twine upload dist/*
