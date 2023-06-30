import fileinput

try:
    import click
except ImportError:
    import sys

    print(
        """"The `antimeridian` command line interface depends on the click package.
Re-install the package with the 'cli' optional dependency:

    pip install 'antimeridian[cli]'

"""
    )
    sys.exit(1)


import json
from typing import Optional

import shapely.geometry

import antimeridian


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("infile", type=str)
@click.option(
    "--force-north-pole",
    is_flag=True,
    show_default=True,
    default=False,
    help="Force the fixed polygon to enclose the north pole",
)
@click.option(
    "--force-south-pole",
    is_flag=True,
    show_default=True,
    default=False,
    help="Force the fixed polygon to enclose the south pole",
)
@click.option(
    "--fix-winding/--no-fix-winding",
    show_default=True,
    default=True,
    help=(
        "Automatically fix clockwise polygons to be the correct counterclockwise "
        "winding order"
    ),
)
def fix(
    infile: str, force_north_pole: bool, force_south_pole: bool, fix_winding: bool
) -> None:
    """Fixes any antimeridian problems a GeoJSON file

    Writes the fixed GeoJSON to standard output. If the filename is ``-`` the
    input GeoJSON is read from standard input.
    """
    data = ""
    with fileinput.input(infile) as f:
        for line in f:
            data += line + "\n"
    fixed = antimeridian.fix_geojson(
        json.loads(data),
        force_north_pole=force_north_pole,
        force_south_pole=force_south_pole,
        fix_winding=fix_winding,
    )
    print(json.dumps(fixed))


@cli.command()
@click.argument("infile", type=str)
@click.option(
    "-i", "--index", help="Return the single LineString at this index", type=int
)
def segment(infile: str, index: Optional[int]) -> None:
    """Segments the exterior coordinates of a GeoJSON file

    Prints the resulting MultiLineString to standard output. Useful mostly for
    debugging problems with `fix`.
    """
    with open(infile) as f:
        data = json.load(f)
    segments = antimeridian.segment_geojson(data)
    if index is not None:
        data = shapely.geometry.mapping(segments.geoms[index])
    else:
        data = shapely.geometry.mapping(segments)
    print(json.dumps(data))
