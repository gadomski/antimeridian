import json
from pathlib import Path
from typing import Callable

import pytest
import shapely.geometry

from antimeridian import GeoInterface

TEST_DATA_DIRECTORY = Path(__file__).parent / "data"
INPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "input"
OUTPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "output"


@pytest.fixture
def read_input() -> Callable[[str], GeoInterface]:
    def read_input(name: str) -> GeoInterface:
        return read_file((INPUT_DATA_DIRECTORY / name).with_suffix(".json"))

    return read_input


@pytest.fixture
def read_output() -> Callable[[str], GeoInterface]:
    def read_output(name: str) -> GeoInterface:
        return read_file((OUTPUT_DATA_DIRECTORY / name).with_suffix(".json"))

    return read_output


def read_file(path: Path) -> GeoInterface:
    with open(path) as f:
        data = json.load(f)
    shape = shapely.geometry.shape(data)
    return shape
