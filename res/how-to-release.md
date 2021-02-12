# How to release

- Switch to latest `main` branch
- Get latest changelog via `make changelog`, edit `CHANGELOG.md` file and commit
- Bump version number in `setup.py`, e.g., `0.0.2` and commit
- Push all changes and check [Github Actions](https://github.com/BastiTee/pype-cli/actions) for successful builds
- Tag release with `git tag 0.0.2`
- Push all changes: `git push --tags && git push`
- Trigger Github action to release to PyPi
