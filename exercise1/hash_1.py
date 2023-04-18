# Funkcje hashujące

from dataclasses import dataclass
from simple_cryptography import hash


@dataclass
class Transaction:
    id: int
    target_id: int
    metadata: str

    def hash(self) -> bytes:
        transaction_bytes = self.id.to_bytes(2, 'big') +\
            self.target_id.to_bytes(2, byteorder='big') + \
            bytes(self.metadata, encoding='utf-8')
        
        return hash(transaction_bytes)
