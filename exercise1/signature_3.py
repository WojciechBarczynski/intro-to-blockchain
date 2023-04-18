from simple_cryptography import (
    PublicKey,
    sign,
    verify_signature,
    generate_key_pair,
    hash,
)


UMOWA = """
Zgadzam się na wszystko
1. aaaaaaa
2. bbbbbb
3. ccccccc
4. dddddddd
"""


class Alice:
    def __init__(self):
        self._public_key, self._private_key = generate_key_pair()

    def sign(self) -> bytes:
        return sign(self._private_key, hash(bytes(UMOWA, 'utf-8')))

    def get_public_key(self) -> PublicKey:
        return self._public_key


class Bob:
    def __init__(self, alice: Alice):
        self.alice = alice

    def validate_signature(self, signature: bytes) -> bool:
        return verify_signature(self.alice.get_public_key(), signature, hash(bytes(UMOWA, 'utf-8')))
