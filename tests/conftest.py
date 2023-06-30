import json
import sys
from pathlib import Path
from typing import Callable, Union

import pytest
import shapely.geometry
from shapely.geometry import (
    GeometryCollection,
    LinearRing,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

TEST_DATA_DIRECTORY = Path(__file__).parent / "data"
INPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "input"
OUTPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "output"

Reader: TypeAlias = Callable[
    [str],
    Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        LinearRing,
        GeometryCollection,
    ],
]


@pytest.fixture
def read_input() -> Reader:
    def read_input(
        name: str,
    ) -> Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        LinearRing,
        GeometryCollection,
    ]:
        return read_file((INPUT_DATA_DIRECTORY / name).with_suffix(".json"))

    return read_input


@pytest.fixture
def input_path() -> Callable[[str], Path]:
    def input_path(name: str) -> Path:
        return (INPUT_DATA_DIRECTORY / name).with_suffix(".json")

    return input_path


@pytest.fixture
def read_output() -> Reader:
    def read_output(
        name: str,
    ) -> Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        LinearRing,
        GeometryCollection,
    ]:
        return read_file((OUTPUT_DATA_DIRECTORY / name).with_suffix(".json"))

    return read_output


def read_file(
    path: Path,
) -> Union[
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    LinearRing,
    GeometryCollection,
]:
    with open(path) as f:
        data = json.load(f)
    shape = shapely.geometry.shape(data)
    return shape
