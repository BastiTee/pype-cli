# How to release

- Switch to latest `main` branch after making sure [it is stable](https://github.com/BastiTee/pype-cli/actions)
- Get latest changelog via `make changelog` and update `CHANGELOG.md`
- Bump version number in `setup.py`, e.g., to `0.0.2`
- Commit all changes with `git commit -am "Release 0.0.2"`
- Tag release with `git tag 0.0.2`
- Push all changes: `git push origin 0.0.2 && git push`
- Trigger [Github action](https://github.com/BastiTee/pype-cli/actions?query=workflow%3ARelease) to release to PyPi
