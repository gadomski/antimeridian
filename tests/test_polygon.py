import antimeridian
import pytest
import shapely.geometry
from antimeridian import FixWindingWarning
from shapely.geometry import MultiPolygon, Polygon

from .conftest import Reader


@pytest.mark.parametrize(
    ("name"),
    [
        "almost-180",
        "complex-split",
        "crossing-latitude",
        "extra-crossing",
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
def test_fix_polygon(
    name: str,
    read_input: Reader,
    read_output: Reader,
) -> None:
    input = read_input(name)
    assert isinstance(input, Polygon)
    output = read_output(name)
    assert isinstance(input, Polygon) or isinstance(input, MultiPolygon)
    fixed = antimeridian.fix_polygon(input).normalize()
    assert fixed == output.normalize()


def test_both_poles(read_input: Reader, read_output: Reader) -> None:
    input = read_input("both-poles")
    assert isinstance(input, Polygon)
    output = read_output("both-poles")
    assert isinstance(input, Polygon)
    fixed = antimeridian.fix_polygon(input, fix_winding=False).normalize()
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
    fixed = antimeridian.fix_polygon(fixed)
    assert fixed.normalize() == output.normalize()


def test_force_north_pole(read_input: Reader, read_output: Reader) -> None:
    input = read_input("force-north-pole")
    output = read_output("force-north-pole")
    fixed = antimeridian.fix_polygon(input, force_north_pole=True)
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("minx,maxx", [(-180, -170), (170, 180)])
def test_dont_segment_antimeridian_overlap(minx: float, maxx: float) -> None:
    shape = shapely.geometry.box(minx=minx, miny=-10, maxx=maxx, maxy=10)
    fixed = antimeridian.fix_polygon(shape)
    assert fixed.geom_type == "Polygon"


@pytest.mark.parametrize("name", ("cw-only", "cw-split"))
def test_fix_winding(read_input: Reader, read_output: Reader, name: str) -> None:
    input = read_input(name)
    output = read_output(name)
    with pytest.warns(FixWindingWarning):
        fixed = antimeridian.fix_polygon(input)
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("name", ("cw-only", "cw-split"))
def test_no_fix_winding(read_input: Reader, read_output: Reader, name: str) -> None:
    input = read_input(name)
    output = read_output(f"{name}-no-fix")
    fixed = antimeridian.fix_polygon(input, fix_winding=False)
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("name", ("cw-only", "cw-split"))
@pytest.mark.parametrize(
    "force_north_pole,force_south_pole", [(True, False), (False, True), (True, True)]
)
def test_no_fix_winding_when_forcing_poles(
    read_input: Reader,
    read_output: Reader,
    name: str,
    force_north_pole: bool,
    force_south_pole: bool,
) -> None:
    input = read_input(name)
    output = read_output(f"{name}-no-fix")
    fixed = antimeridian.fix_polygon(
        input,
        force_north_pole=force_north_pole,
        force_south_pole=force_south_pole,
    )
    assert fixed.normalize() == output.normalize()


def test_fix_winding_interior_no_segments(read_input: Reader) -> None:
    input = read_input("simple-with-ccw-hole")
    with pytest.warns(FixWindingWarning):
        fixed = antimeridian.fix_polygon(input)
    assert all(not shapely.is_ccw(interior) for interior in fixed.interiors)


def test_fix_winding_interior_segments(read_input: Reader, read_output: Reader) -> None:
    input = read_input("one-ccw-hole")
    output = read_output("one-hole")
    with pytest.warns(FixWindingWarning):
        fixed = antimeridian.fix_polygon(input)
    assert fixed.normalize() == output.normalize()
