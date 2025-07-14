# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.2] - 2025-07-14

### Fixed

- Multiple interiors ([#172](https://github.com/gadomski/antimeridian/pull/172))

## [0.4.1] - 2025-04-10

### Added

- Reverse argument ([#167](https://github.com/gadomski/antimeridian/pull/167))

## [0.4.0] - 2024-12-17

### Added

- Optional `--no-great-circle` option to CLI ([#153](https://github.com/gadomski/antimeridian/issues/153))
- Optional `great_circle` argument to geometry-fixing functions ([#153](https://github.com/gadomski/antimeridian/issues/153))

### Changed

- Default method for finding meridian crossings now relies on spherical geometry ([#153](https://github.com/gadomski/antimeridian/issues/153))

## [0.3.12] - 2024-12-09

### Changed

- Documentation updates for [JOSS paper](https://github.com/openjournals/joss-reviews/issues/7530).

## [0.3.11] - 2024-10-17

### Fixed

- Bounding boxes for globe-spanning geometries ([#150](https://github.com/gadomski/antimeridian/pull/150))

## [0.3.10] - 2024-10-17

### Added

- `bbox` subcommand to CLI ([#148](https://github.com/gadomski/antimeridian/pull/148))

## [0.3.9] - 2024-10-12

### Added

- `force_over_antimeridian` argument to `bbox` ([#142](https://github.com/gadomski/antimeridian/pull/142))

## [0.3.8] - 2024-07-11

### Fixed

- Forcing the north or the south pole wasn't working in some cases ([#125](https://github.com/gadomski/antimeridian/pull/125))

## [0.3.7] - 2024-06-20

### Fixed

- `__geo_interface` is a property ([#121](https://github.com/gadomski/antimeridian/pull/121))

## [0.3.6] - 2024-05-16

### Fixed

- Preserve z coordinates ([#116](https://github.com/gadomski/antimeridian/pull/116))

## [0.3.5] - 2024-05-05

### Fixed

- Correct the case when neighboring points are on 180 and -180 and are not part of a latitude band ([#114](https://github.com/gadomski/antimeridian/pull/114))

## [0.3.4] - 2024-03-29

### Fixed

- Project url ([#106](https://github.com/gadomski/antimeridian/issues/106))

## [0.3.3] - 2023-08-21

### Fixed

- Wrapping of centroid points ([#69](https://github.com/gadomski/antimeridian/pull/69))

## [0.3.2] - 2023-08-21

### Added

- `centroid` ([#67](https://github.com/gadomski/antimeridian/pull/67))

## [0.3.1] - 2023-07-10

### Added

- Read from standard input in the CLI ([#48](https://github.com/gadomski/antimeridian/pull/48))
- Support for line strings and multi-line strings ([#50](https://github.com/gadomski/antimeridian/pull/50))

### Fixed

- Don't produce meaningless splits when one corner of an input polygon is on the antimeridian ([#49](https://github.com/gadomski/antimeridian/pull/49))
- Correct tiny floating point deltas on the antimeridian ([#52](https://github.com/gadomski/antimeridian/pull/52))

## [0.3.0] - 2023-06-29

### Changed

- Clockwise input polygons are reversed by default, though this behavior can be overridden ([#39](https://github.com/gadomski/antimeridian/pull/39))

## [0.2.6] - 2023-05-31

### Fixed

- Don't segment polygons that simply overlap the antimeridian ([#37](https://github.com/gadomski/antimeridian/pull/37))

## [0.2.5] - 2023-05-31

### Added

- Calculate spec-conforming bounding boxes ([#35](https://github.com/gadomski/antimeridian/pull/35))

## [0.2.4] - 2023-05-12

### Fixed

- Minimum shapely version needs to be 2.0 ([#27](https://github.com/gadomski/antimeridian/pull/27))

## [0.2.3] - 2023-04-28

## Fixed

- Unused arguments in `fix_multi_polygon` ([#21](https://github.com/gadomski/antimeridian/pull/21))

## [0.2.2] - 2023-04-28

### Added

- Boolean flags to force a polygon to enclose the north or south poles ([#17](https://github.com/gadomski/antimeridian/pull/17))

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

[unreleased]: https://github.com/gadomski/antimeridian/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/gadomsk/antimeridian/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/gadomsk/antimeridian/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/gadomsk/antimeridian/compare/v0.3.12...v0.4.0
[0.3.12]: https://github.com/gadomsk/antimeridian/compare/v0.3.11...v0.3.12
[0.3.11]: https://github.com/gadomsk/antimeridian/compare/v0.3.10...v0.3.11
[0.3.10]: https://github.com/gadomsk/antimeridian/compare/v0.3.9...v0.3.10
[0.3.9]: https://github.com/gadomsk/antimeridian/compare/v0.3.8...v0.3.9
[0.3.8]: https://github.com/gadomsk/antimeridian/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/gadomsk/antimeridian/compare/v0.3.6...v0.3.7
[0.3.6]: https://github.com/gadomsk/antimeridian/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/gadomsk/antimeridian/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/gadomsk/antimeridian/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/gadomsk/antimeridian/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/gadomsk/antimeridian/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/gadomsk/antimeridian/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/gadomsk/antimeridian/compare/v0.2.6...v0.3.0
[0.2.6]: https://github.com/gadomsk/antimeridian/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/gadomsk/antimeridian/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/gadomsk/antimeridian/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/gadomsk/antimeridian/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/gadomsk/antimeridian/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/gadomsk/antimeridian/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/gadomsk/antimeridian/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/gadomsk/antimeridian/compare/v0.0.2...v0.1.0
[0.0.2]: https://github.com/gadomsk/antimeridian/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/gadomski/antimeridian/releases/tag/v0.0.1

<!-- markdownlint-disable-file MD024 -->
