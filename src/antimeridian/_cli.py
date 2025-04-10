import sys

try:
    import click
except ImportError:
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
from click import File

import antimeridian


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("infile", type=File("r"), default=sys.stdin)
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
@click.option(
    "--great-circle/--no-great-circle",
    show_default=True,
    default=True,
    help="Compute meridian crossings on the sphere rather than using 2D geometry",
)
@click.option(
    "--reverse",
    show_default=True,
    default=False,
    is_flag=True,
    help="Reverse the coordinates before fixing",
)
def fix(
    infile: File,
    force_north_pole: bool,
    force_south_pole: bool,
    fix_winding: bool,
    great_circle: bool,
    reverse: bool,
) -> None:
    """Fixes any antimeridian problems a GeoJSON file

    Writes the fixed GeoJSON to standard output. If the filename is ``-`` the
    input GeoJSON is read from standard input.
    """
    fixed = antimeridian.fix_geojson(
        json.load(infile),  # type: ignore
        force_north_pole=force_north_pole,
        force_south_pole=force_south_pole,
        fix_winding=fix_winding,
        great_circle=great_circle,
        reverse=reverse,
    )
    print(json.dumps(fixed))


@cli.command()
@click.argument("infile", type=File("r"), default=sys.stdin)
@click.option(
    "-i", "--index", help="Return the single LineString at this index", type=int
)
@click.option(
    "--great-circle/--no-great-circle",
    show_default=True,
    default=True,
    help="Compute meridian crossings on the sphere rather than using 2D geometry",
)
def segment(infile: File, index: Optional[int], great_circle: bool) -> None:
    """Segments the exterior coordinates of a GeoJSON file

    Prints the resulting MultiLineString to standard output. Useful mostly for
    debugging problems with `fix`.
    """
    data = json.load(infile)  # type: ignore
    segments = antimeridian.segment_geojson(data, great_circle)
    if index is not None:
        data = shapely.geometry.mapping(segments.geoms[index])
    else:
        data = shapely.geometry.mapping(segments)
    print(json.dumps(data))


@cli.command()
@click.argument("infile", type=File("r"), default=sys.stdin)
@click.option(
    "-f",
    "--force-over-antimeridian",
    help="Force the bbox to be antimeridian-spanning",
    type=bool,
)
def bbox(infile: File, force_over_antimeridian: bool) -> None:
    """Calculates the antimeridian-spanning bbox for the input geometry."""
    shape = json.load(infile)  # type: ignore
    print(json.dumps(antimeridian.bbox(shape)))
