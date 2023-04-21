# Releasing

1. Determine the next version. Try to follow [semantic versioning](https://semver.org/).
   Our public API is every importable Python function and class, except for `antimeridian.main` -- the CLI is not part of the API, and can break at any time.
2. Update:
   - The version in [pyproject.toml](./pyproject.toml)
   - The [CHANGELOG](./CHANGELOG.md)
   - The **pre-commit** hooks: `pre-commit autoupdate`
3. Open a PR with the changes named `release/vX.Y.Z`.
4. When the PR is merged, created a tag on `main` with that version with a `v` prefix, e.g. `vX.Y.Z`.
5. Push the tag to Github, which will fire off the release workflow.
