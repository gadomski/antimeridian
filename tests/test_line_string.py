import antimeridian

from .conftest import Reader


def test_line_string(read_input: Reader, read_output: Reader) -> None:
    input = read_input("line")
    output = read_output("line")
    fixed = antimeridian.fix_line_string(input)
    assert fixed.is_valid
    assert fixed.normalize() == output.normalize()


def test_multi_line_string(read_input: Reader, read_output: Reader) -> None:
    input = read_input("multi-line")
    output = read_output("multi-line")
    fixed = antimeridian.fix_multi_line_string(input)
    assert fixed.is_valid
    assert fixed.normalize() == output.normalize()
