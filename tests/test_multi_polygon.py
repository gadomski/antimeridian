import pytest
import shapely.geometry
from shapely.geometry import MultiPolygon

import antimeridian

from .conftest import Reader


@pytest.mark.parametrize(
    ("name"),
    [
        "multi-split",
        "multi-no-antimeridian",
    ],
)
def test_multi_polygon(
    read_input: Reader,
    read_output: Reader,
    name: str,
) -> None:
    input = read_input(name)
    assert isinstance(input, MultiPolygon)
    output = read_output(name)
    assert isinstance(output, MultiPolygon)
    fixed = antimeridian.fix_multi_polygon(input)
    assert fixed.is_valid
    assert fixed.normalize() == output.normalize()


def test_fix_shape(read_input: Reader) -> None:
    # Just a smoke test
    input = shapely.geometry.mapping(read_input("multi-split"))
    antimeridian.fix_shape(input)
