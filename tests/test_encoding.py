from app.core.decode import decode
from app.core.encode import encode
import pytest

@pytest.mark.parametrize("n",[0, 1, 61, 62, 3844, 999999, 238328] + list(range(5000)))
def test_roundtrip(n):
    assert decode(encode(n)) == str(n)

