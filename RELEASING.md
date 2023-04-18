# Releasing

1. Determine the next version. Try to follow [semantic versioning](https://semver.org/).
   Our public API is every importable Python function and class, except for `antimeridian.main` -- the CLI is not part of the API, and can break at any time.
2. Update the version in [pyproject.toml](./pyproject.toml), update the [CHANGELOG](./CHANGELOG.md), and open a PR with the changes named `release/vX.Y.Z`.
3. When the PR is merged, created a tag on `main` with that version with a `v` prefix, e.g. `vX.Y.Z`.
4. Push the tag to Github, which will fire off the release workflow.
