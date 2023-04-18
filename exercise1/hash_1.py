# Funkcje hashujące

from dataclasses import dataclass
from simple_cryptography import hash


@dataclass
class Transaction:
    id: int
    target_id: int
    metadata: str

    def hash(self) -> bytes:
        transaction_bytes = int.to_bytes(self.id, 'big') + \
            int.to_bytes(self.target_id, 'big') + \
            bytes(self.metadata, 'utf-8')
        
        return hash(transaction_bytes)
