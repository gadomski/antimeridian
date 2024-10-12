# Releasing

1. Determine the next version.
   We adhere to [semantic versioning](https://semver.org/).
   Our public API is every importable Python function and class, except for `antimeridian.main` -- the CLI is not part of the API, and can break at any time.
2. Create a branch named `release/vX.Y.Z`.
3. Update:
   - The version in [pyproject.toml](./pyproject.toml)
   - The [CHANGELOG](./CHANGELOG.md)
   - The **pre-commit** hooks:
      - `pre-commit autoupdate`
      - Update any `additional_dependencies` fields to match `pyproject.toml`
4. Open a PR with the changes
5. When the PR is merged, created a tag on `main` with that version with a `v` prefix, e.g. `vX.Y.Z`.
6. Push the tag to Github, which will fire off the release workflow.
7. Create a release via [the Github interface](https://github.com/gadomski/antimeridian/releases).
