# How to release

## Prerequisites

-   Install `git` and the `git-flow` extension (`brew install git-flow-avh`)
-   Checkout `master` and `develop` branch
-   Initialize git flow using `git flow init` (all branches set with default values)

## Process

-   Switch to latest `develop` branch
-   Finish development and push all changes
-   Check [Github Actions](https://github.com/BastiTee/pype-cli/actions) for successful builds
-   Run a full build: `make`
-   Start release, e.g., for release 0.0.1: `git flow release start 0.0.1`
-   Get latest changelog via `make changelog`, edit CHANGELOG file and commit
-   Finish release: `git flow release finish --tagname 0.0.1 0.0.1`
-   Bump version to next version in setup.py, e.g., `0.0.2`
-   Commit version bump
-   Push all changes: `git push --tags && git push`
-   Check [Github Actions](https://github.com/BastiTee/pype-cli/actions) for successful builds
-   Push to PyPi using `git checkout master && make publish && git checkout develop`
