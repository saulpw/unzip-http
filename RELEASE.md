# Release Process

## To release a new version

1. Update `version` in `pyproject.toml`
2. Add entry to `CHANGELOG.md`
3. Commit: `git commit -am "release vX.Y"`
4. Tag: `git tag vX.Y`
5. Push: `git push && git push --tags`

GitHub Actions will automatically build and publish to PyPI when the tag is pushed.

## One-time setup (already done)

To enable automated PyPI publishing via trusted publishers (OIDC, no API tokens):

1. **PyPI**: Go to the [unzip-http project settings](https://pypi.org/manage/project/unzip-http/settings/publishing/), add a trusted publisher:
   - Owner: `saulpw`
   - Repository: `unzip-http`
   - Workflow: `publish.yml`
   - Environment: `pypi`

2. **GitHub**: In repo Settings → Environments, create an environment called `pypi`.
