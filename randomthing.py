
"""Provides a clear example of how the random function is pseudorandom -- and will create a
reliable reproduction of a string of items if the seed is known."""

from random import Random


def encode(s: str, seed: int) -> str:
    data = Random()
    data.seed(seed)

    result = bytearray([ord(c) ^ data.randrange(256) for c in s])
    return result.hex().upper()


def decode(s: str, seed: int):
    data = Random()
    data.seed(seed)
    return ''.join(chr(c ^ data.randrange(256)) for c in bytes.fromhex(s))


if __name__ == "__main__":
    message = "magic"
    encrypted = encode(message, 1234)
    decrypted = decode(encrypted, 1234)
    print(encrypted, decrypted)
