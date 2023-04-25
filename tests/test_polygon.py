import antimeridian
import pytest
import shapely.geometry
from shapely.geometry import MultiPolygon, Polygon

from .conftest import Reader


@pytest.mark.parametrize(
    ("name"),
    [
        "both-poles",
        "complex-split",
        "crossing-latitude",
        "extra-crossing",
        "latitude-band",
        "north-pole",
        "one-hole",
        "over-180",
        "overlap",
        "simple",
        "south-pole",
        "split",
        "two-holes",
    ],
)
def test_fix_polygon(
    name: str,
    read_input: Reader,
    read_output: Reader,
) -> None:
    input = read_input(name)
    assert isinstance(input, Polygon)
    output = read_output(name)
    assert isinstance(input, Polygon | MultiPolygon)
    fixed = antimeridian.fix_polygon(input).normalize()
    assert fixed == output.normalize()


def test_fix_shape(read_input: Reader) -> None:
    # Just a smoke test
    input = shapely.geometry.mapping(read_input("simple"))
    antimeridian.fix_shape(input)


def test_double_fix(
    read_input: Reader,
    read_output: Reader,
) -> None:
    input = read_input("north-pole")
    output = read_output("north-pole")
    fixed = antimeridian.fix_polygon(input)
    fixed = antimeridian.fix_polygon(input)
    assert fixed.normalize() == output.normalize()
