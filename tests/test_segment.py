import antimeridian

from .conftest import Reader


def test_segment(read_input: Reader) -> None:
    input = read_input("split")
    segments = antimeridian.segment_shape(input)
    assert len(segments) == 2
