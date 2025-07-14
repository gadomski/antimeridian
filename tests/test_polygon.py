from typing import cast

import pytest
import shapely.affinity
import shapely.geometry
from shapely.geometry import MultiPolygon, Point, Polygon

import antimeridian
from antimeridian import FixWindingWarning

from .conftest import Reader


@pytest.mark.parametrize(
    ("name"),
    [
        "almost-180",
        "complex-split",
        "crossing-latitude",
        "extra-crossing",
        "issues-81",
        "issues-171",
        "latitude-band",
        "north-pole",
        "one-hole",
        "over-180",
        "overlap",
        "point-on-antimeridian",
        "simple",
        "south-pole",
        "split",
        "two-holes",
    ],
)
@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_fix_polygon(
    name: str,
    read_input: Reader,
    read_output: Reader,
    subdirectory: str,
    great_circle: bool,
) -> None:
    input = read_input(name)
    assert isinstance(input, Polygon)
    output = read_output(name, subdirectory)
    assert isinstance(input, Polygon) or isinstance(input, MultiPolygon)
    fixed = antimeridian.fix_polygon(input, great_circle=great_circle).normalize()
    assert fixed == output.normalize()


@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_both_poles(
    read_input: Reader, read_output: Reader, subdirectory: str, great_circle: bool
) -> None:
    input = read_input("both-poles")
    assert isinstance(input, Polygon)
    output = read_output("both-poles", subdirectory)
    assert isinstance(input, Polygon)
    fixed = antimeridian.fix_polygon(
        input, fix_winding=False, great_circle=great_circle
    ).normalize()
    assert fixed == output.normalize()


def test_fix_shape(read_input: Reader) -> None:
    # Just a smoke test
    input = shapely.geometry.mapping(read_input("simple"))
    antimeridian.fix_shape(input)


@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_double_fix(
    read_input: Reader,
    read_output: Reader,
    subdirectory: str,
    great_circle: bool,
) -> None:
    input = read_input("north-pole")
    output = read_output("north-pole", subdirectory)
    fixed = antimeridian.fix_polygon(input, great_circle=great_circle)
    fixed = antimeridian.fix_polygon(fixed, great_circle=great_circle)
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_force_north_pole(
    read_input: Reader, read_output: Reader, subdirectory: str, great_circle: bool
) -> None:
    input = read_input("force-north-pole")
    output = read_output("force-north-pole", subdirectory)
    fixed = antimeridian.fix_polygon(
        input, force_north_pole=True, great_circle=great_circle
    )
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("minx,maxx", [(-180, -170), (170, 180)])
def test_dont_segment_antimeridian_overlap(minx: float, maxx: float) -> None:
    shape = shapely.geometry.box(minx=minx, miny=-10, maxx=maxx, maxy=10)
    fixed = antimeridian.fix_polygon(shape)
    assert fixed.geom_type == "Polygon"


@pytest.mark.parametrize("name", ("cw-only", "cw-split"))
@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_fix_winding(
    read_input: Reader,
    read_output: Reader,
    name: str,
    subdirectory: str,
    great_circle: bool,
) -> None:
    input = read_input(name)
    output = read_output(name, subdirectory)
    with pytest.warns(FixWindingWarning):
        fixed = antimeridian.fix_polygon(input, great_circle=great_circle)
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("name", ("cw-only", "cw-split"))
@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_no_fix_winding(
    read_input: Reader,
    read_output: Reader,
    name: str,
    subdirectory: str,
    great_circle: bool,
) -> None:
    input = read_input(name)
    output = read_output(f"{name}-no-fix", subdirectory)
    fixed = antimeridian.fix_polygon(
        input, fix_winding=False, great_circle=great_circle
    )
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("name", ("cw-only", "cw-split"))
@pytest.mark.parametrize(
    "force_north_pole,force_south_pole", [(True, False), (False, True), (True, True)]
)
@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_no_fix_winding_when_forcing_poles(
    read_input: Reader,
    read_output: Reader,
    name: str,
    force_north_pole: bool,
    force_south_pole: bool,
    subdirectory: str,
    great_circle: bool,
) -> None:
    input = read_input(name)
    output = read_output(f"{name}-no-fix", subdirectory)
    fixed = antimeridian.fix_polygon(
        input,
        force_north_pole=force_north_pole,
        force_south_pole=force_south_pole,
        great_circle=great_circle,
    )
    assert fixed.normalize() == output.normalize()


def test_fix_winding_interior_no_segments(read_input: Reader) -> None:
    input = read_input("simple-with-ccw-hole")
    with pytest.warns(FixWindingWarning):
        fixed = antimeridian.fix_polygon(input)
    assert all(not shapely.is_ccw(interior) for interior in fixed.interiors)


def test_fix_winding_interior_segments(read_input: Reader, read_output: Reader) -> None:
    input = read_input("one-ccw-hole")
    output = read_output("one-hole", "spherical")
    with pytest.warns(FixWindingWarning):
        fixed = antimeridian.fix_polygon(input)
    assert fixed.normalize() == output.normalize()


def test_centroid_simple(read_input: Reader) -> None:
    input = read_input("simple")
    centroid = cast(Point, antimeridian.centroid(input))
    assert centroid.x == 95
    assert centroid.y == 45


def test_centroid_split(read_output: Reader) -> None:
    input = read_output("split")
    centroid = cast(Point, antimeridian.centroid(input))
    assert centroid.x == 180
    assert centroid.y == 45


def test_centroid_split_with_shift(read_input: Reader) -> None:
    input = read_input("split")
    input = shapely.affinity.translate(input, xoff=+1)
    input = antimeridian.fix_polygon(input, great_circle=False)
    centroid = cast(Point, antimeridian.centroid(input))
    assert centroid.x == -179
    assert centroid.y == 45


def test_z_coordinates() -> None:
    # https://github.com/gadomski/antimeridian/issues/115
    polygon = Polygon([[0, 0, 1], [10, 0, 2], [10, 10, 3], [0, 10, 4]])
    fixed = antimeridian.fix_polygon(polygon)
    assert fixed.has_z


@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_force_south_pole(
    read_input: Reader, read_output: Reader, subdirectory: str, great_circle: bool
) -> None:
    # https://github.com/gadomski/antimeridian/issues/124
    input = read_input("issues-124")
    output = read_output("issues-124", subdirectory)
    fixed = antimeridian.fix_polygon(
        input, force_south_pole=True, great_circle=great_circle
    )
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize(
    "subdirectory,great_circle", (("flat", False), ("spherical", True))
)
def test_great_circle(
    read_input: Reader, read_output: Reader, subdirectory: str, great_circle: bool
) -> None:
    # https://github.com/gadomski/antimeridian/issues/153
    input = read_input("great-circle")
    output = read_output("great-circle", subdirectory)
    fixed = antimeridian.fix_polygon(input, great_circle=great_circle)
    assert fixed.normalize() == output.normalize()
