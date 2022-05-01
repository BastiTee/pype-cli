# Required executables
ifeq (, $(shell which python))
 $(error "No python on PATH.")
endif
PIPENV_CMD := python -m pipenv
PIP_CMD := python -m pip
ifeq (, $(shell $(PIPENV_CMD) --version))
 $(error "No $(PIPENV_CMD) on PATH.")
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
PY_FILES := setup.py pype tests

all: prepare build

prepare: clean
	@echo Preparing virtual environment
	$(PIPENV_CMD) install --dev
	mkdir -p $(PYPE_CONFIG_FOLDER)
	echo "export PYPE_CONFIG_FOLDER=$(PYPE_CONFIG_FOLDER)" >> .venv/bin/activate

build: test mypy isort lint
	@echo Run setup.py-based build process to package application
	$(PIPENV_CMD) run python setup.py bdist_wheel

shell:
	@echo Initialize virtualenv and open a new shell using it
	$(PIPENV_CMD) shell

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
	-name "pyproject.toml" -o \
	-name "Pipfile.lock" \
	|xargs rm -rfv

test:
	@echo Run all tests in default virtualenv
	$(PIPENV_CMD) run py.test --verbose tests

isort:
	@echo Check for incorrectly sorted imports
	$(PIPENV_CMD) run isort --check-only $(PY_FILES)

isort-apply:
	@echo Check for incorrectly sorted imports
	$(PIPENV_CMD) run isort $(PY_FILES)

lint:
	@echo Run code formatting checks against source code base
	$(PIPENV_CMD) run flake8 $(PY_FILES)

mypy:
	@echo Run static code checks against source code base
	$(PIPENV_CMD) run mypy pype tests

sys-info:
	@echo Print pype configuration within venv
	$(PIPENV_CMD) run pype pype.config system-info

install-wheel: all
	@echo Install from wheel
	$(PIP_CMD) install --force-reinstall dist/*.whl

install-wheel-no-test:
	@echo Install from wheel including rebuild but skipping tests
	rm -rf dist/*.whl
	$(PIPENV_CMD) run python setup.py bdist_wheel
	$(PIP_CMD) install --force-reinstall dist/*.whl

publish: all
	@echo Publish pype to pypi.org
	TWINE_USERNAME=$(TWINE_USERNAME) TWINE_PASSWORD=$(TWINE_PASSWORD) \
	$(PIPENV_CMD) run twine upload dist/*

release:
	@echo Commit release - requires NEXT_VERSION to be set
	test $(NEXT_VERSION)
	sed -i '' "s/version='[0-9\.]*',/version='$(NEXT_VERSION)',/" setup.py
	git commit -am "Release $(NEXT_VERSION)"
	git tag $(NEXT_VERSION)
	git push origin $(NEXT_VERSION)
	git push

changelog:
	@echo Return changelog since last version tag
	git --no-pager log --pretty=format:"- %s" $(VERSION_HASH)..HEAD |cat
