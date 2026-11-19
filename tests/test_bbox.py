import pytest
from shapely.geometry import MultiPolygon, box

import antimeridian

from .conftest import Reader


@pytest.mark.parametrize(
    "name,expected",
    [
        ("simple", [90, 40, 100, 50]),
        ("split", [170, 40, -170, 50]),
        ("multi-no-antimeridian", [90, 10, 100, 50]),
        ("north-pole", [-180, 40, 180, 90]),
        ("ocean", [-180, -85.609, 180, 90]),
    ],
)
def test_bbox(read_output: Reader, name: str, expected: list[float]) -> None:
    shape = read_output(name)
    bbox = antimeridian.bbox(shape)
    assert bbox == expected


def test_bbox_force_over_antimeridian(read_output: Reader) -> None:
    expected = [
        179.96779787822723,
        -19.044135782844712,
        -179.77058698198195,
        -18.555752850452095,
    ]
    shape = read_output("issues-134")
    bbox = antimeridian.bbox(shape, force_over_antimeridian=True)
    assert bbox == expected


def test_bbox_islands_input(read_input: Reader) -> None:
    shape = read_input("bbox-islands")
    assert antimeridian.bbox(shape) == [170, 0, -140, 2.5]


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize(
    "intervals,expected",
    [
        ([(-180, -175), (-150, -140), (170, 180)], [170, -140]),
        ([(-180, -170), (140, 150), (175, 180)], [140, -170]),
        ([(-180, -170), (-5, 5), (170, 180)], [-5, -170]),
        ([(-180, 100), (-160, -150), (120, 130), (160, 180)], [160, 130]),
        ([(-180, -100), (-110, 100), (90, 180)], [-180, 180]),
        ([(-180, 0), (0, 180)], [-180, 180]),
    ],
)
def test_bbox_contains_all_islands(
    intervals: list[tuple[float, float]], expected: list[float], reverse: bool
) -> None:
    # Different latitudes keep the polygons disjoint even when their longitude
    # ranges overlap. A bounding box must contain the whole ranges, not just vertices.
    polygons = [box(west, i, east, i + 0.5) for i, (west, east) in enumerate(intervals)]
    shape = MultiPolygon(polygons[::-1] if reverse else polygons)
    assert shape.is_valid

    west, south, east, north = antimeridian.bbox(shape)
    assert [west, south, east, north] == [
        expected[0],
        0,
        expected[1],
        len(polygons) - 0.5,
    ]
    if west > east:
        coverage = box(west, south, 180, north).union(box(-180, south, east, north))
    else:
        coverage = box(west, south, east, north)
    assert coverage.covers(shape)


@pytest.mark.parametrize("force", [False, True])
def test_bbox_detached_islands_force_over_antimeridian(force: bool) -> None:
    shape = MultiPolygon(
        [box(-179, 0, -175, 1), box(-150, 2, -140, 3), box(170, 4, 179, 5)]
    )

    assert antimeridian.bbox(shape, force_over_antimeridian=force) == (
        [170, 0, -140, 5] if force else [-179, 0, 179, 5]
    )
