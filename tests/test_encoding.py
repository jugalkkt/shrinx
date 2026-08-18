from app.core.decode import decode
from app.core.encode import encode

def test_roundtrip():
    assert decode(encode("3844")) == "3844"
