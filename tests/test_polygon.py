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
        "simple",
        "south-pole",
        "split",
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


def test_fix_polygon_with_interior_fails() -> None:
    polygon = Polygon(
        shell=((0, 0), (30, 0), (30, 30), (0, 30), (0, 0)),
        holes=[((10, 10), (20, 10), (20, 20), (10, 20), (10, 10))],
    )
    with pytest.raises(ValueError):
        antimeridian.fix_polygon(polygon)


def test_fix_shape(read_input: Callable[[str], GeoInterface]) -> None:
    # Just a smoke test
    input = shapely.geometry.mapping(read_input("simple"))
    antimeridian.fix_shape(input)
