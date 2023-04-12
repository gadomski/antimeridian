import json
from pathlib import Path
from typing import List, Tuple

import pytest
import shapely.geometry
from shapely.geometry import MultiPolygon, Polygon

import antimeridian

TEST_DATA_DIRECTORY = Path(__file__).parent / "data"
INPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "input"
OUTPUT_DATA_DIRECTORY = TEST_DATA_DIRECTORY / "output"
NAMES = [
    "both-poles",
    "complex-split",
    "crossing-latitude",
    "extra-crossing",
    "north-pole",
    "simple",
    "south-pole",
    "split",
]


def read_file(path: Path) -> Polygon | MultiPolygon:
    with open(path) as f:
        data = json.load(f)
    shape = shapely.geometry.shape(data)
    assert isinstance(shape, Polygon) or isinstance(shape, MultiPolygon)
    return shape


def read_input_file(name: str) -> Polygon:
    return read_file(INPUT_DATA_DIRECTORY / f"{name}.json")


def read_output_file(name: str) -> Polygon:
    return read_file(OUTPUT_DATA_DIRECTORY / f"{name}.json")


def inputs_and_outputs(
    names: List[str],
) -> List[Tuple[Polygon, Polygon | MultiPolygon]]:
    inputs_and_outputs = list()
    for name in names:
        inputs_and_outputs.append((read_input_file(name), read_output_file(name)))
    return inputs_and_outputs


@pytest.mark.parametrize(("input", "output"), inputs_and_outputs(NAMES), ids=NAMES)
def test_close_polygon(input: Polygon, output: Polygon | MultiPolygon) -> None:
    closed = antimeridian.fix_polygon(input).normalize()
    assert closed.is_valid
    assert closed == output.normalize()


def test_close_polygon_with_interior_fails() -> None:
    polygon = Polygon(
        shell=((0, 0), (30, 0), (30, 30), (0, 30), (0, 0)),
        holes=[((10, 10), (20, 10), (20, 20), (10, 20), (10, 10))],
    )
    with pytest.raises(ValueError):
        antimeridian.fix_polygon(polygon)


def test_fix_shape() -> None:
    shape = {
        "type": "Polygon",
        "coordinates": [[[100, 40], [100, 50], [90, 50], [90, 40], [100, 40]]],
    }
    antimeridian.fix_shape(shape)


def test_fix_not_a_polygon() -> None:
    shape = {"type": "Point", "coordinates": [100, 40]}
    with pytest.raises(ValueError):
        antimeridian.fix_shape(shape)
