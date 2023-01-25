import hashlib

from sha256 import sha224, sha256, sha512


def test_0bit(test: bytes = b"") -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest(), "sha256 failed on 0bit test"
    assert sha224(test) == hashlib.sha224(test).hexdigest(), "sha224 failed on 0bit test"
    assert sha512(test) == hashlib.sha512(test).hexdigest(), "sha512 failed on 0bit test"


def test_24bit(test: bytes = b"???") -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest(), "sha256 failed on 24bit test"
    assert sha224(test) == hashlib.sha224(test).hexdigest(), "sha224 failed on 24bit test"
    assert sha512(test) == hashlib.sha512(test).hexdigest(), "sha512 failed on 24bit test"


def test_448bit(test: bytes = b"abcdbcdecdefdefgef!hfghighijh jkijkljklmklmnlmn`mnopnopq") -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest(), "sha256 failed on 448bit test"
    assert sha224(test) == hashlib.sha224(test).hexdigest(), "sha224 failed on 448bit test"
    assert sha512(test) == hashlib.sha512(test).hexdigest(), "sha512 failed on 448bit test"


def test_896bit(test: bytes = b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu") -> None:  # noqa
    assert sha256(test) == hashlib.sha256(test).hexdigest(), "sha256 failed on 896bit test"
    assert sha224(test) == hashlib.sha224(test).hexdigest(), "sha224 failed on 896bit test"
    assert sha512(test) == hashlib.sha512(test).hexdigest(), "sha512 failed on 896bit test"


def test_1millionbit(test: bytes = b"!" * 125_000) -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest(), "sha256 failed on 1million bit test"
    assert sha224(test) == hashlib.sha224(test).hexdigest(), "sha224 failed on 1million bit test"
    assert sha512(test) == hashlib.sha512(test).hexdigest(), "sha512 failed on 1million bit test"


def test_8millionbit(test: bytes = b" " * 1_000_000) -> None:
    assert sha256(test) == hashlib.sha256(test).hexdigest(), "sha256 failed on 8million bit test"
    assert sha224(test) == hashlib.sha224(test).hexdigest(), "sha224 failed on 8million bit test"
    assert sha512(test) == hashlib.sha512(test).hexdigest(), "sha512 failed on 8million bit test"
