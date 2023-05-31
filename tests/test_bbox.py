from typing import List

import antimeridian
import pytest

from .conftest import Reader


@pytest.mark.parametrize(
    "name,expected",
    [
        ("simple", [90, 40, 100, 50]),
        ("split", [170, 40, -170, 50]),
        ("multi-no-antimeridian", [90, 10, 100, 50]),
        ("north-pole", [-180, 40, 180, 90]),
    ],
)
def test_bbox(read_output: Reader, name: str, expected: List[float]) -> None:
    shape = read_output(name)
    bbox = antimeridian.bbox(shape)
    assert bbox == expected
