import pytest

import antimeridian

from .conftest import Reader


@pytest.mark.parametrize("great_circle", [True, False])
def test_line_string(
    read_input: Reader, read_output: Reader, great_circle: bool
) -> None:
    input = read_input("line")
    output = read_output("line")
    fixed = antimeridian.fix_line_string(input, great_circle)
    assert fixed.is_valid
    assert fixed.normalize() == output.normalize()


@pytest.mark.parametrize("great_circle", [True, False])
def test_multi_line_string(
    read_input: Reader, read_output: Reader, great_circle: bool
) -> None:
    input = read_input("multi-line")
    output = read_output("multi-line")
    fixed = antimeridian.fix_multi_line_string(input, great_circle)
    assert fixed.is_valid
    assert fixed.normalize() == output.normalize()
