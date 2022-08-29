# Implemented from the pseudocode at https://en.wikipedia.org/wiki/SHA-2

from typing import Generator


__all__ = ["sha224", "sha256", "sha512"]


def _rr(x: int, n: int, *, bit_size: int = 32, mask: int = 0xFFFFFFFF) -> int:
    return ((x >> n) | (x << (bit_size - n))) & mask


def __sha224_constants() -> tuple[int, int, int, int, int, int, int, int, list[int]]:
    h0 = 0xc1059ed8
    h1 = 0x367cd507
    h2 = 0x3070dd17
    h3 = 0xf70e5939
    h4 = 0xffc00b31
    h5 = 0x68581511
    h6 = 0x64f98fa7
    h7 = 0xbefa4fa4

    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    return (h0, h1, h2, h3, h4, h5, h6, h7, k)


def __sha256_constants() -> tuple[int, int, int, int, int, int, int, int, list[int]]:
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    return (h0, h1, h2, h3, h4, h5, h6, h7, k)


def __sha512_constants() -> tuple[int, int, int, int, int, int, int, int, list[int]]:
    h0 = 0x6a09e667f3bcc908
    h1 = 0xbb67ae8584caa73b
    h2 = 0x3c6ef372fe94f82b
    h3 = 0xa54ff53a5f1d36f1
    h4 = 0x510e527fade682d1
    h5 = 0x9b05688c2b3e6c1f
    h6 = 0x1f83d9abfb41bd6b
    h7 = 0x5be0cd19137e2179

    k = [
        0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538,
        0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe,
        0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
        0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
        0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab,
        0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
        0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed,
        0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
        0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
        0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53,
        0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373,
        0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
        0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c,
        0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6,
        0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
        0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
    ]

    return (h0, h1, h2, h3, h4, h5, h6, h7, k)


def __int_from_bytes(message: bytes) -> int:
    L = len(message)
    x = 0

    for (i, c) in enumerate(message):
        x |= (c << ((L - i - 1) * 8))

    return x


def __pad(message: bytes, *, pad_size: int = 512) -> int:
    L = len(message) * 8
    return ((__int_from_bytes(message) << 1) | 1) << ((pad_size + (pad_size // 8)) - ((1 + (pad_size // 8) + L) % pad_size)) | L


def __isolate(value: int, nbits: int, *, start_bit: int = 0) -> int:
    return (value & (((1 << nbits) - 1) << start_bit)) >> (start_bit)


def __chunk(padded: int, *, chunk_size: int = 512) -> Generator[int, None, None]:
    for i in range(((padded.bit_length() + 1) // chunk_size) - 1, -1, -1):
        yield __isolate(padded, chunk_size, start_bit=(i * chunk_size))


def sha224(message: bytes) -> str:
    h0, h1, h2, h3, h4, h5, h6, h7, k = __sha224_constants()

    for chunk in __chunk(__pad(message), chunk_size=512):
        w = [0] * 64

        for i in range(15, -1, -1):
            w[15 - i] = __isolate(chunk, 32, start_bit=(i * 32))

        for i in range(16, 64):
            s0 = _rr(w[i - 15], 7) ^ _rr(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = _rr(w[i - 2], 17) ^ _rr(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(64):
            S1 = _rr(e, 6) ^ _rr(e, 11) ^ _rr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            t1 = (h + S1 + ch + k[i] + w[i]) & 0xFFFFFFFF
            S0 = _rr(a, 2) ^ _rr(a, 13) ^ _rr(a, 22)
            ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = (S0 + ma) & 0xFFFFFFFF

            h, g, f, e, d, c, b, a = g, f, e, (d + t1) & 0xFFFFFFFF, c, b, a, (t1 + t2) & 0xFFFFFFFF

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    digest = 0

    for i, v in enumerate([h0, h1, h2, h3, h4, h5, h6]):
        digest += v << ((6 - i) * 32)

    return hex(digest)[2:]


def sha256(message: bytes) -> str:
    h0, h1, h2, h3, h4, h5, h6, h7, k = __sha256_constants()

    for chunk in __chunk(__pad(message), chunk_size=512):
        w = [0] * 64

        for i in range(15, -1, -1):
            w[15 - i] = __isolate(chunk, 32, start_bit=(i * 32))

        for i in range(16, 64):
            s0 = _rr(w[i - 15], 7) ^ _rr(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = _rr(w[i - 2], 17) ^ _rr(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(64):
            S1 = _rr(e, 6) ^ _rr(e, 11) ^ _rr(e, 25)
            ch = (e & f) ^ ((~e) & g)
            t1 = (h + S1 + ch + k[i] + w[i]) & 0xFFFFFFFF
            S0 = _rr(a, 2) ^ _rr(a, 13) ^ _rr(a, 22)
            ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = (S0 + ma) & 0xFFFFFFFF

            h, g, f, e, d, c, b, a = g, f, e, (d + t1) & 0xFFFFFFFF, c, b, a, (t1 + t2) & 0xFFFFFFFF

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    digest = 0

    for i, v in enumerate([h0, h1, h2, h3, h4, h5, h6, h7]):
        digest += v << ((7 - i) * 32)

    return hex(digest)[2:]


def sha512(message: bytes) -> str:
    h0, h1, h2, h3, h4, h5, h6, h7, k = __sha512_constants()

    for chunk in __chunk(__pad(message, pad_size=1024), chunk_size=1024):
        w = [0] * 80

        for i in range(15, -1, -1):
            w[15 - i] = __isolate(chunk, 64, start_bit=(i * 64))

        for i in range(16, 80):
            s0 = _rr(w[i - 15], 1, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ _rr(w[i - 15], 8, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ (w[i - 15] >> 7)
            s1 = _rr(w[i - 2], 19, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ _rr(w[i - 2], 61, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ (w[i - 2] >> 6)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFFFFFFFFFF

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(80):
            S1 = _rr(e, 14, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ _rr(e, 18, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ _rr(e, 41, bit_size=64, mask=0xFFFFFFFFFFFFFFFF)  # noqa
            ch = (e & f) ^ ((~e) & g)
            t1 = (h + S1 + ch + k[i] + w[i]) & 0xFFFFFFFFFFFFFFFF
            S0 = _rr(a, 28, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ _rr(a, 34, bit_size=64, mask=0xFFFFFFFFFFFFFFFF) ^ _rr(a, 39, bit_size=64, mask=0xFFFFFFFFFFFFFFFF)  # noqa
            ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = (S0 + ma) & 0xFFFFFFFFFFFFFFFF

            h, g, f, e, d, c, b, a = g, f, e, (d + t1) & 0xFFFFFFFFFFFFFFFF, c, b, a, (t1 + t2) & 0xFFFFFFFFFFFFFFFF

        h0 = (h0 + a) & 0xFFFFFFFFFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFFFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFFFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFFFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFFFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFFFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFFFFFFFFFF

    digest = 0

    for i, v in enumerate([h0, h1, h2, h3, h4, h5, h6, h7]):
        digest += v << ((7 - i) * 64)

    return hex(digest)[2:]
