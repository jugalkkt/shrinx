from app.core.shortcode import generate_code
import pytest

@pytest.mark.parametrize("n",[7, 12])
def test_roundtrip(n):
    assert  len(generate_code(n)) == n