from time import time
from typing import Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from simple_cryptography import PublicKey, verify_signature

# Spróbuj zmodyfikować liczbę i zobacz, jak wpłynie to na czas wydobywania bloku!
DIFFICULTY = 1e72


class Node:
    """
    Klasa reprezentująca węzeł sieci. Odpowiada za dodawanie transakcji i tworzenie bloków.
    Powinna zawierać:
    - blockchain,
    - klucz publiczny właściciela, wykorzystywany do przypisywania nowych coin'ów do konta.
    """
    blockchain: Blockchain
    owner: PublicKey

    def __init__(self, owner_public_key: PublicKey, initial_transaction: Transaction):
        """
        Przypisz wartości polom owner oraz blockchain przy pomocy podanych argumentów.
        Wykorzystaj `initial_transaction` do stworzenia blockchain (hash poprzedniego bloku i nonce powinny być zerem).

        """
        self.owner = owner_public_key
        self.blockchain = Blockchain([Block(b'\x00', int(time()), 0, [initial_transaction])])

    def add_transaction(self, transaction: Transaction):
        """
        Sprawdź, czy transakcja jest poprawna (użyj metody `validate_transaction`), jeśli nie jest, rzuć wyjątek.
        Stwórz transakcję generującą nowego coin'a, aby wynagrodzić właściciela node'a.
        Stwórz nowy blok zawierający obie transakcje.
        Znajdź nonce, który spełni kryteria sieci (użyj metody `find_nonce`).
        Dodaj blok na koniec łańcucha.
        """
        if not self.validate_transaction(transaction):
            raise Exception("Transaction can't be added. Verification failed.")

        new_coin_transaction = Transaction(recipient=self.owner, previous_tx_hash=b'\x00')
        new_block = Block(
            prev_block_hash=self.blockchain.get_latest_block().hash,
            timestamp=int(time()),
            nonce=0,
            transactions=[transaction, new_coin_transaction]
        )

        new_block = self.find_nonce(new_block)
        self.blockchain.blocks.append(new_block)

    def find_nonce(self, block: Block) -> Optional[Block]:
        """
        Znajdź nonce spełniające kryterium -> hash bloku powinien być mniejszy niż zadana liczba.
        """
        while int.from_bytes(block.hash, 'big') > DIFFICULTY:
            block.nonce += 1
        return block

    def validate_transaction(self, transaction: Transaction) -> bool:
        """
        Transakcja jest poprawna, jeśli ma podpis, podpis jest poprawny oraz coin,
        którego chcemy wydać, istnieje i nie został wcześniej wydany.
        Skorzystaj z funkcji `verify_signature` z modułu simple_cryptography.
        """
        if transaction.signature is None:
            return False

        prev_transaction = self.blockchain.get_transaction(transaction.previous_tx_hash)
        if prev_transaction is None:
            return False

        if self.blockchain.get_transaction_by_previous_tx_hash(prev_transaction.tx_hash) is not None:
            return False

        return verify_signature(
            prev_transaction.recipient,
            transaction.signature,
            transaction.tx_hash
        )

    def get_state(self) -> Blockchain:
        """
        Zwróć blockchain.
        """
        return self.blockchain


def validate_chain(chain: Blockchain) -> bool:
    """
    Łańcuch jest poprawny, jeśli dla każdego bloku (poza zerowym):
    - hash poprzedniego bloku jest przypisany prawidłowo,
    - wykonano proof of work (hash bloku spełnia kryterium, jest mniejszy niż zadana liczba).
    """
    for index, block in enumerate(chain.blocks[1:]):
        if block.prev_block_hash != chain.blocks[index].hash:
            return False

        if int.from_bytes(block.hash, 'big') > DIFFICULTY:
            return False

    return True
