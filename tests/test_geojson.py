import copy

import pytest
import shapely.geometry

import antimeridian

from .conftest import Reader


@pytest.mark.parametrize("great_circle", [True, False])
def test_fix_feature(read_input: Reader, great_circle: bool) -> None:
    input = read_input("simple")
    feature = {"type": "Feature", "geometry": input, "properties": {"foo": "bar"}}
    fixed = antimeridian.fix_geojson(feature, great_circle=great_circle)
    assert fixed["properties"]["foo"] == "bar"


@pytest.mark.parametrize("great_circle", [True, False])
def test_fix_feature_collection(read_input: Reader, great_circle: bool) -> None:
    input = read_input("simple")
    feature_a = {
        "type": "Feature",
        "geometry": copy.deepcopy(input),
        "properties": {"foo": "bar"},
    }
    feature_b = {"type": "Feature", "geometry": input, "properties": {"baz": "boz"}}
    feature_collection = {
        "type": "FeatureCollection",
        "features": [feature_a, feature_b],
        "another": "property",
    }
    fixed = antimeridian.fix_geojson(feature_collection, great_circle=great_circle)
    assert fixed["features"][0]["properties"]["foo"] == "bar"
    assert fixed["features"][1]["properties"]["baz"] == "boz"
    assert fixed["another"] == "property"


@pytest.mark.parametrize("great_circle", [True, False])
def test_segment_feature(read_input: Reader, great_circle: bool) -> None:
    input = read_input("split")
    feature = {"type": "Feature", "geometry": input}
    fixed = antimeridian.segment_geojson(feature, great_circle)
    assert len(fixed.geoms) == 2


@pytest.mark.parametrize(
    "subdirectory,great_circle",
    [("flat", False), ("spherical", True)],
)
def test_reverse(
    read_input: Reader, read_output: Reader, subdirectory: str, great_circle: bool
) -> None:
    input = read_input("issues-164")
    feature = {"type": "Feature", "geometry": input}
    fixed = antimeridian.fix_geojson(feature, reverse=True, great_circle=great_circle)
    assert (
        shapely.geometry.shape(fixed["geometry"]).normalize()
        == read_output("issues-164", subdirectory).normalize()
    )
