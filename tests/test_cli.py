import json
from collections.abc import Callable
from pathlib import Path

import pytest
from pytest_console_scripts import ScriptRunner

import antimeridian

from .conftest import OUTPUT_DATA_DIRECTORY

pytest.importorskip("click")


def test_fix(script_runner: ScriptRunner, input_path: Callable[[str], Path]) -> None:
    path = input_path("simple")
    result = script_runner.run(["antimeridian", "fix", str(path)])
    assert result.success


def test_segment(
    script_runner: ScriptRunner, input_path: Callable[[str], Path]
) -> None:
    path = input_path("simple")
    result = script_runner.run(["antimeridian", "segment", str(path)])
    assert result.success


@pytest.mark.parametrize(
    "options,forced",
    [
        (["-f", "{path}"], True),
        (["{path}", "-f"], True),
        (["{path}"], False),
    ],
)
def test_bbox_force_over_antimeridian(
    script_runner: ScriptRunner, options: list[str], forced: bool
) -> None:
    path = OUTPUT_DATA_DIRECTORY / "flat" / "issues-134.json"
    shape = json.loads(path.read_text())
    # The forced bbox must differ from the default for this to test anything.
    assert antimeridian.bbox(shape, True) != antimeridian.bbox(shape)
    args = [option.format(path=path) for option in options]
    result = script_runner.run(["antimeridian", "bbox", *args])
    assert result.success
    assert json.loads(result.stdout) == antimeridian.bbox(shape, forced)
