# Releasing

1. Determine the next version. Try to follow [semantic versioning](https://semver.org/).
   Our public API is every importable Python function and class, except for `antimeridian.main` -- the CLI is not part of the API, and can break at any time.
2. Update the [CHANGELOG](./CHANGELOG.md) and commit the update.
3. Create a tag with that version, with a `v` prefix, e.g. `v1.2.3`.
4. Push the tag and the new commit to Github.
5. Use [workflow dispatch](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch) to start the [Release workflow](https://github.com/gadomski/antimeridian/actions/workflows/release.yaml).
