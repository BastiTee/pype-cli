# Required executables
ifeq (, $(shell which python3))
 $(error "No python3 on PATH.")
endif
ifeq (, $(shell which pipenv))
 $(error "No pipenv on PATH.")
endif

# Suppress warning if pipenv is started inside .venv
export PIPENV_VERBOSITY = 1
# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT = 1
# Ignore existing venvs
export PIPENV_IGNORE_VIRTUALENVS = 1
# Make sure we are running with an explicit encoding
export LC_ALL = C
export LANG = C.UTF-8
# Set configuration folder to venv
export PYPE_CONFIG_FOLDER = $(shell pwd)/.venv/.pype-cli
# Process variables
LAST_VERSION := $(shell git tag | sort --version-sort -r | head -n1)
VERSION_HASH := $(shell git show-ref -s $(LAST_VERSION))
PY_FILES := setup.py pype tests example_pypes
DOCKER_IMAGE := pype-docker-mint-install

all: prepare build

prepare: clean
	@echo Preparing virtual environment
	pipenv install --dev
	mkdir -p $(PYPE_CONFIG_FOLDER)
	echo "export PYPE_CONFIG_FOLDER=$(PYPE_CONFIG_FOLDER)" >> .venv/bin/activate

build: test mypy isort lint
	@echo Run setup.py-based build process to package application
	pipenv run python setup.py bdist_wheel

shell:
	@echo Initialize virtualenv and open a new shell using it
	pipenv shell

clean:
	@echo Clean project base
	find . -type d \
	-name ".venv" -o \
	-name ".ropeproject" -o \
	-name "build" -o \
	-name "dist" -o \
	-name "__pycache__" -o \
	-name ".mypy_cache" -o \
	-name ".pytest_cache" -o \
	-iname "*.egg-info" -o \
	-name "src" \
	|xargs rm -rfv

	find . -type f \
	-name "pyproject.toml" \
	|xargs rm -rfv

test:
	@echo Run all tests in default virtualenv
	pipenv run py.test --verbose tests

isort:
	@echo Check for incorrectly sorted imports
	pipenv run isort --check-only $(PY_FILES)

isort-apply:
	@echo Check for incorrectly sorted imports
	pipenv run isort $(PY_FILES)

lint:
	@echo Run code formatting checks against source code base
	pipenv run flake8 $(PY_FILES)

mypy:
	@echo Run static code checks against source code base
	pipenv run mypy pype example_pypes tests

sys-info:
	@echo Print pype configuration within venv
	pipenv run pype pype.config system-info

install-wheel: all
	@echo Install from wheel
	pip3 install --force-reinstall dist/*.whl

dockerize: build
	@echo Install pype into a dockercontainer to test mint installation
	docker build -t $(DOCKER_IMAGE) .
	docker run -ti --rm $(DOCKER_IMAGE)

publish: all
	@echo Publish pype to pypi.org
	TWINE_USERNAME=$(TWINE_USERNAME) TWINE_PASSWORD=$(TWINE_PASSWORD) \
	pipenv run twine upload dist/*

changelog:
	@echo Return changelog since last version tag
	git --no-pager log --pretty=format:"- %s" $(VERSION_HASH)..HEAD |cat
