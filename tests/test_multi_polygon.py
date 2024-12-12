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
@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_multi_polygon(
    read_input: Reader,
    read_output: Reader,
    name: str,
    subdirectory: str,
    great_circle: bool,
) -> None:
    input = read_input(name)
    assert isinstance(input, MultiPolygon)
    output = read_output(name, subdirectory)
    assert isinstance(output, MultiPolygon)
    fixed = antimeridian.fix_multi_polygon(input, great_circle=great_circle)
    assert fixed.is_valid
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("great_circle", [True, False])
def test_fix_shape(read_input: Reader, great_circle: bool) -> None:
    # Just a smoke test
    input = shapely.geometry.mapping(read_input("multi-split"))
    antimeridian.fix_shape(input, great_circle=great_circle)
