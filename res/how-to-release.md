# How to release

- Switch to latest `main` branch after making sure [it is stable](https://github.com/BastiTee/pype-cli/actions)
- Get latest changelog via `make changelog`, edit `CHANGELOG.md` file and commit
- Bump version number in `setup.py`, e.g., `0.0.2` and commit
- Tag release with `git tag 0.0.2`
- Push all changes: `git push origin 0.0.2 && git push`
- Trigger Github action to release to PyPi
