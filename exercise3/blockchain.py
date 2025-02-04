from typing import List, Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block


class Blockchain:
    """
    Klasa reprezentująca łańcuch bloków.
    Powinna zawierać:
    - listę bloków.
    """

    blocks: List[Block]

    def __init__(self, initial_transaction: Transaction):
        initial_block = Block(
            prev_block_hash=b"\x00", transactions=[initial_transaction], nonce=0
        )
        self.blocks = [initial_block]

    def get_latest_block(self) -> Block:
        """
        Zwróć ostatni blok.
        """
        return self.blocks[-1]

    def length(self) -> int:
        """
        Zwróć długość łańcucha.
        """
        return len(self.blocks)

    def get_tx_by_hash(self, tx_hash: bytes) -> Optional[Transaction]:
        """
        Przy pomocy hasha wyszukaj transakcję.
            Przechodząc po wszystkich blokach i ich transakcjach zwróć pasującą transakcję.
            Jeśli transakcja o podanym hashu nie istnieje zwróć None.
        """
        for block in self.blocks:
            for tx in block.transactions:
                if tx.hash == tx_hash:
                    return tx
        return None


    def get_tx_by_previous_tx_hash(
        self, previous_tx_hash: bytes
    ) -> Optional[Transaction]:
        """
        Wyszukaj transakcję o polu previous_tx_hash równym temu podanemu w argumencie.
            Przechodząc po wszystkich blokach i ich transakcjach zwróć pasującą transakcję.
            Jeśli transakcja z podanym previous_tx_hash nie istnieje zwróć None.
        """
        for block in self.blocks:
            for tx in block.transactions:
                if tx.previous_tx_hash == previous_tx_hash:
                    return tx
                
        return None

