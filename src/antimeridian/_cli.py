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
def fix(infile: str) -> None:
    """Fixes any antimeridian problems a GeoJSON file

    Writes the fixed GeoJSON to standard output.
    """
    with open(infile) as f:
        data = json.load(f)
    fixed = antimeridian.fix_geojson(data)
    print(json.dumps(fixed))


@cli.command()
@click.argument("infile", type=str)
@click.option(
    "-i", "--index", help="Return the single LineString at this index", type=int
)
def segment(infile: str, index: Optional[int]) -> None:
    """Segments the exterior coordinates of a GeoJSON file

    Prints the resulting MultiLineString to standard output.
    """
    with open(infile) as f:
        data = json.load(f)
    segments = antimeridian.segment_geojson(data)
    if index is not None:
        data = shapely.geometry.mapping(segments.geoms[index])
    else:
        data = shapely.geometry.mapping(segments)
    print(json.dumps(data))
