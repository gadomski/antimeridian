import warnings

import pytest
import shapely.geometry
from shapely.geometry import MultiPolygon, Polygon

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


def test_force_both_poles(read_input: Reader, read_output: Reader) -> None:
    # Forcing a pole disables winding correction, like fix_polygon.
    input = read_input("both-poles")
    assert isinstance(input, Polygon)
    output = read_output("both-poles")
    fixed = antimeridian.fix_multi_polygon(
        MultiPolygon([input]),
        force_north_pole=True,
        force_south_pole=True,
        great_circle=False,
    )
    assert fixed.normalize() == MultiPolygon([output]).normalize()


@pytest.mark.parametrize("name", ["split", "cw-split", "issues-174"])
@pytest.mark.parametrize(
    "force_north_pole,force_south_pole", [(True, False), (False, True), (True, True)]
)
@pytest.mark.parametrize("great_circle", [False, True])
def test_force_pole_matches_fix_polygon(
    read_input: Reader,
    name: str,
    force_north_pole: bool,
    force_south_pole: bool,
    great_circle: bool,
) -> None:
    input = read_input(name)
    assert isinstance(input, Polygon)
    kwargs = dict(
        force_north_pole=force_north_pole,
        force_south_pole=force_south_pole,
        great_circle=great_circle,
    )
    expected = antimeridian.fix_polygon(input, **kwargs)
    if isinstance(expected, Polygon):
        expected = MultiPolygon([expected])
    fixed = antimeridian.fix_multi_polygon(MultiPolygon([input]), **kwargs)
    assert fixed.normalize() == expected.normalize()


def test_force_pole_does_not_warn_about_winding(read_input: Reader) -> None:
    input = read_input("cw-only")
    assert isinstance(input, Polygon)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        antimeridian.fix_multi_polygon(MultiPolygon([input]), force_north_pole=True)
