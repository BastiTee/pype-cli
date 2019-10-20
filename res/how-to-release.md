# How to release

## Prerequisites

- Install `git` and the `git-flow` extension
- Checkout `master` and `develop` branch
- Initialize git flow using `git flow init` (all branches set with default values)

## Process

- Switch to latest `develop` branch
- Finish development and push all changes
- Check [Travis](https://travis-ci.org/BastiTee/pype/branches) for successful builds
- Run a full build: `./make build`
- Start release, e.g., for release 0.0.1: `git flow release start 0.0.1`
- Finish release by..
  - getting the latest changelog via `./make changelog` and edit CHANGELOG file
- Finish release: `git flow release finish --tagname 0.0.1 0.0.1`
- Bump version to next version in setup.py, e.g., `0.0.2`
- Push all changes: `git push --tags && git push`
- Check [Travis](https://travis-ci.org/BastiTee/pype/branches) for successful builds
- Push to PyPi using `./make publish`
