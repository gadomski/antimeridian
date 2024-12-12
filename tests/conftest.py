import json
from collections.abc import Callable
from pathlib import Path
from typing import Protocol, Union

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

TEST_DATA_DIRECTORY = Path(__file__).parent / "data"
INPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "input"
OUTPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "output"


class Reader(Protocol):
    def __call__(
        self, name: str, subdirectory: str | None = None
    ) -> Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        LinearRing,
        GeometryCollection,
    ]: ...


@pytest.fixture
def read_input() -> Reader:
    def read_input(
        name: str,
        subdirectory: str | None = None,
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
        path = Path(subdirectory) / name if subdirectory is not None else Path(name)
        return read_file((INPUT_DATA_DIRECTORY / path).with_suffix(".json"))

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
        subdirectory: str | None = "flat",
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
        path = Path(subdirectory) / name if subdirectory is not None else Path(name)
        return read_file((OUTPUT_DATA_DIRECTORY / path).with_suffix(".json"))

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
