from typing import List

import pytest

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
def test_bbox(read_output: Reader, name: str, expected: List[float]) -> None:
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
