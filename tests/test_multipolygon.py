from typing import Callable

import shapely.geometry
from shapely.geometry import MultiPolygon

import antimeridian
from antimeridian import GeoInterface


def test_multi_polygon(
    read_input: Callable[[str], GeoInterface],
    read_output: Callable[[str], GeoInterface],
) -> None:
    input = read_input("multi-split")
    assert isinstance(input, MultiPolygon)
    output = read_output("multi-split")
    assert isinstance(output, MultiPolygon)
    fixed = antimeridian.fix_multi_polygon(input)
    assert fixed.is_valid
    assert fixed.normalize() == output.normalize()


def test_fix_shape(read_input: Callable[[str], GeoInterface]) -> None:
    # Just a smoke test
    input = shapely.geometry.mapping(read_input("multi-split"))
    antimeridian.fix_shape(input)
