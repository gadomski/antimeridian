import pytest

import antimeridian

from .conftest import Reader


@pytest.mark.parametrize("great_circle", [True, False])
def test_segment(read_input: Reader, great_circle: bool) -> None:
    input = read_input("split")
    segments = antimeridian.segment_shape(input, great_circle)
    assert len(segments) == 2


@pytest.mark.parametrize("great_circle", [True, False])
def test_fix_feature_collection(read_input: Reader, great_circle: bool) -> None:
    input = read_input("split")
    feature = {
        "type": "Feature",
        "geometry": input,
    }
    feature_collection = {
        "type": "FeatureCollection",
        "features": [feature],
        "another": "property",
    }
    segments = antimeridian.segment_geojson(
        feature_collection, great_circle=great_circle
    )
    assert len(segments.geoms)
