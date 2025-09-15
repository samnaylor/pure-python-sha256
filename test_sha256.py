from typing import Any

import pytest

from sha256 import sha224, sha256, sha512

algorithms = {
    "sha224": sha224,
    "sha256": sha256,
    "sha512": sha512,
}


@pytest.mark.parametrize(
    "alg,data,expected",
    [
        ("sha224", b"", "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"),
        ("sha224", b"", "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"),
        ("sha224", b"abc", "23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7"),
        ("sha224", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "75388b16512776cc5dba5da1fd890150b0c6455cb4f58b1952522525"),
        ("sha224", b"a" * 1000000, "20794655980c91d8bbb4c1ea97618a4bf03f42581948b2ee4ee7ad67"),
        ("sha256", b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("sha256", b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("sha256", b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
        ("sha256", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
        ("sha256", b"a" * 1000000, "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"),
        (
            "sha512",
            b"",
            "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce" + "47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",
        ),
        (
            "sha512",
            b"abc",
            "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a" + "2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f",
        ),
        (
            "sha512",
            b"abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn" + b"hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu",
            "8e959b75dae313da8cf4f72814fc143f8f7779c6eb9f7fa17299aeadb6889018" + "501d289e4900f7e4331b99dec4b5433ac7d329eeb6dd26545e96e55b874be909",
        ),
        (
            "sha512",
            b"a" * 1000000,
            "e718483d0ce769644e2e42c7bc15b4638e1f98b13b2044285632a803afa973eb" + "de0ff244877ea60a4cb0432ce577c31beb009c5c2c49aa2e4eadb217ad8cc09b",
        ),
    ],
)
def test_hash(benchmark: Any, alg: str, data: bytes, expected: str) -> None:
    assert benchmark(lambda: algorithms[alg](data)) == expected
