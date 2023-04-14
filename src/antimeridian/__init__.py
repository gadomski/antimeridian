"""Fix antimeridian crossings in GeoJSON objects and shapely geometries."""

from ._implementation import (
    GeoInterface,
    fix_geojson,
    fix_multi_polygon,
    fix_polygon,
    fix_shape,
)


def main() -> int:
    """Runs :py:func:`fix_geojson` on a file (or standard input) and print the
    result to standard output.

    Returns:
        The exit code.
    """

    import fileinput
    import json
    import sys
    from pathlib import Path

    name = Path(sys.argv[0]).stem
    if len(sys.argv) > 2:
        print("ERROR: more than one argument provided")
        print(f"USAGE: {name} [filename]")
        return 1
    elif len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print(
            f"""Fixes antimeridian issues in GeoJSON geometries.

The output geometry will be printed to standard output. No formatting options
are provided; use jq (https://stedolan.github.io/jq/) or another, similar tool
to format any output.

See https://github.com/gadomski/antimeridian for more information on the
underlying algorithm.

# Usage

Reads GeoJSON from a file and redirect it into a new file:

    {name} polygon.json > fixed.json

Reads GeoJSON from standard input and prints it to standard output:

    {name} -

Prints this help:

    {name}
    {name} -h
    {name} --help
"""
        )
        return 0

    input = ""
    for line in fileinput.input(sys.argv[1]):
        input += line
    data = json.loads(input)
    fixed = fix_geojson(data)
    print(json.dumps(fixed))
    return 0


__all__ = [
    "fix_polygon",
    "fix_geojson",
    "fix_multi_polygon",
    "fix_shape",
    "GeoInterface",
]
__version__ = "0.0.1"
