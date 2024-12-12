import pytest

import antimeridian

from .conftest import Reader


@pytest.mark.parametrize("great_circle", [True, False])
def test_segment(read_input: Reader, great_circle: bool) -> None:
    input = read_input("split")
    segments = antimeridian.segment_shape(input, great_circle)
    assert len(segments) == 2
