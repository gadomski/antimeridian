# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2023-04-28

### Added

- Support for unsplit clockwise inputs ([#13](https://github.com/gadomski/antimeridian/pull/13))
- More documentation ([#14](https://github.com/gadomski/antimeridian/pull/14))

## [0.2.0] - 2023-04-26

### Added

- Segmentation functions to the public API ([#12](https://github.com/gadomski/antimeridian/pull/12))
- click-based command line interface ([#12](https://github.com/gadomski/antimeridian/pull/12))

### Fixed

- Protect against longitudes outside of 180 or -180 ([#8](https://github.com/gadomski/antimeridian/pull/8))

### Removed

- The ability to run the module as a script via `__main__` ([#12](https://github.com/gadomski/antimeridian/pull/12))

## [0.1.0] - 2023-04-18

This v0.1.0 release is to indicate that we think that this package is ready to use!

### Removed

- **setuptools-scm**, it was too fragile ([#2](https://github.com/gadomski/antimeridian/pull/2))

## [0.0.2] - 2023-04-14

### Added

- `__main__`
- This changelog and releasing instructions
- Readthedocs

### Changed

- `local_scheme` for setuptools-scm

### Removed

- `examples/fix.py`

## [0.0.1] - 2023-04-14

Initial release.

[unreleased]: https://github.com/gadomski/antimeridian/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/gadomsk/antimeridian/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/gadomsk/antimeridian/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/gadomsk/antimeridian/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/gadomsk/antimeridian/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/gadomski/antimeridian/releases/tag/v0.0.1
