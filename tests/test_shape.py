import pytest

import antimeridian


def test_fix_shape() -> None:
    # Just a smoke test
    input = {
        "type": "Polygon",
        "coordinates": [[[100, 40], [100, 50], [90, 50], [90, 40], [100, 40]]],
    }
    antimeridian.fix_shape(input)


def test_fix_not_a_polygon() -> None:
    shape = {"type": "Point", "coordinates": [100, 40]}
    with pytest.raises(ValueError):
        antimeridian.fix_shape(shape)
