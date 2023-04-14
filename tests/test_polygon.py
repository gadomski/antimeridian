from typing import Callable

import pytest
import shapely.geometry
from shapely.geometry import MultiPolygon, Polygon

import antimeridian
from antimeridian import GeoInterface


@pytest.mark.parametrize(
    ("name"),
    [
        "both-poles",
        "complex-split",
        "crossing-latitude",
        "extra-crossing",
        "north-pole",
        "one-hole",
        "simple",
        "south-pole",
        "split",
        "two-holes",
    ],
)
def test_fix_polygon(
    name: str,
    read_input: Callable[[str], GeoInterface],
    read_output: Callable[[str], GeoInterface],
) -> None:
    input = read_input(name)
    assert isinstance(input, Polygon)
    output = read_output(name)
    assert isinstance(input, Polygon | MultiPolygon)
    fixed = antimeridian.fix_polygon(input).normalize()
    assert fixed.is_valid
    assert fixed == output.normalize()


def test_fix_shape(read_input: Callable[[str], GeoInterface]) -> None:
    # Just a smoke test
    input = shapely.geometry.mapping(read_input("simple"))
    antimeridian.fix_shape(input)
