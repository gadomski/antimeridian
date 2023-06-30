from pathlib import Path
from typing import Callable

import pytest
from pytest_console_scripts import ScriptRunner

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
