# How to release

Work in progress.

## Prerequisites

- Install `git` and `git-flow`
- Checkout `master` and `develop` branch
- Switch to `develop` branch
- Initialize git flow using `git flow init` (all branches set with default values)

## Process

- Finish development on develop branch and push all changes
- Check [Travis](https://travis-ci.org/BastiTee/pype/branches) for successful builds
- Run a full build: `./make build`
- Start release: `git flow release start "0.0.1"`
- Finish release by..
  - setting version tag correctly in setup.py and commit change `git add . && git commit -m "Fix version tag"`
  - get the latest changelog via `./make changelog` and edit CHANGELOG file
- Finish release: `git flow release finish "0.0.1"`
- Bump version to next snapshot version in setup.py, e.g., `0.0.2`
- Push all changes: `git push`
- Check [Travis](https://travis-ci.org/BastiTee/pype/branches) for successful builds
- Draft new release in github with tag https://github.com/BastiTee/pype/releases/new << This should happen automatically on GitHub but it doesn't :/
- Push to PyPi using `./make publish`
