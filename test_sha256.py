import hashlib

from sha256 import sha256


def test_0bit(test: bytes = b"abc") -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest()


def test_24bit(test: bytes = b"abc") -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest()


def test_448bit(test: bytes = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq") -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest()


def test_8millionbit(test: bytes = b"a" * 1_000_000) -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest()
