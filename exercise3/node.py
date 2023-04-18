from typing import Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from simple_cryptography import PublicKey, verify_signature, generate_key_pair

# Spróbuj zmodyfikować `DIFFICULTY` i zobacz, jak wpłynie to na czas wydobywania bloku!
DIFFICULTY = 10  # Oznacza ilość zerowych bitów na początku poszukiwanego hasha
MAX_256_INT = 2**256 - 1


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
            Wykorzystaj `initial_transaction` do stworzenia blockchain.
        """
        self.owner = owner_public_key
        self.blockchain = Blockchain(initial_transaction)

    def validate_transaction(self, transaction: Transaction) -> bool:
        """
        Sprawdź poprawność transakcji.
            Transakcja jest poprawna, jeśli:
            - ma podpis,
            - podpis jest poprawny (`transaction` jest podpisane przez osobę posiadającą coina),
            - coin (transakcja), którego chcemy wydać, istnieje i nie został wcześniej wydany.

        Do weryfikacji podpisu skorzystaj z funkcji `verify_signature` z modułu simple_cryptography.

        Jak sprawdzić, czy coin istnieje?
        Spróbuj znaleźć transakcję, o hashu takim samym jak hash transakcji, którą chcemy wydać.

        Jak sprawdzić, czy coin nie został wcześniej wydany?
        Spróbuj znaleźć transakcję, której previous_tx_hash jest taki sam, jak hash transakcji, którą chcemy wydać.

        !! Ważne !!
        Transakcja, którą chcemy wydać oznacza transakcję poprzednią do tej podanej w argumencie `transaction`.
        """
        if transaction.signature is None:
            return False

        prev_transation = self.blockchain.get_tx_by_hash(
            transaction.previous_tx_hash)

        if prev_transation is None:
            return False

        if self.blockchain.get_tx_by_previous_tx_hash(prev_transation.hash) is not None:
            return False

        return verify_signature(prev_transation.recipient, transaction.signature, transaction.hash)

    def _max_int_shifted_by_difficulty(self):
        """
        liczba, która zapisana na 256 bitach ma `DIFFICULTY` zer na początku a potem same jedynki
        """
        return MAX_256_INT >> DIFFICULTY

    def generate_nonce(self, block: Block) -> Block:
        """
        Wygeneruj (wykop) nonce spełniające kryterium -> hash bloku powinien mieć na początku `DIFFICULTY` zer.

        Jak sprawdzić ilość zer na początku hasha?
        Porównaj hash zrzutowany na int oraz maksymalną wartość inta 256 przesuniętą bitowo o DIFFICULTY.

        Przydatne operacje:
        - int.from_bytes(hash, "big")
        - self._max_int_shifted_by_difficulty()
        """
        while (int.from_bytes(block.hash(), 'big') > self._max_int_shifted_by_difficulty()):
            block.nonce += 1
        return block

    def add_transaction(self, transaction: Transaction):
        """
        Dodaj podaną transakcję do bloku.
            Sprawdź, czy transakcja jest poprawna (użyj metody `validate_transaction`), jeśli nie jest, rzuć wyjątek.
            Stwórz transakcję generującą nowego coin'a, aby wynagrodzić właściciela node'a (previous_tx_hash = b'\x00').
            Stwórz nowy blok zawierający obie transakcje.
            Znajdź nonce, który spełni kryteria sieci (użyj metody `generate_nonce`).
            Dodaj blok na koniec łańcucha.
        """
        if not self.validate_transaction(transaction):
            raise Exception("Not valid transaction. Verification failed")

        new_coin_transation = Transaction(self.owner, b'\x00')

        new_block = Block(
            self.blockchain.get_latest_block().hash(), 
            [transaction, new_coin_transation], 
            0)
        
        self.blockchain.blocks.append(new_block)

    def get_state(self) -> Blockchain:
        """
        Zwróć blockchain.
        """
        return self.blockchain


def validate_chain(chain: Blockchain) -> bool:
    """
    Zweryfikuj poprawność łańcucha.
        Łańcuch jest poprawny, jeśli dla każdego bloku (poza zerowym):
        - hash poprzedniego bloku jest przypisany prawidłowo,
        _ timestamp nie maleje razem z numerem bloku,
        - wykonano proof of work (hash bloku ma na początku `DIFFICULTY` zer),
        - istnieje maksymalnie jedna transkacja tworząca nowego coina,
        - wszystkie transakcje w bloku są poprawne.

        Pamiętaj, że w bloku istnieją transakcje tworzące nowe coiny (nie będą miały one podpisu)!

        Podpowiedź: Dla ułatwienia możesz skonstruować nowego node'a, na bieżąco weryfikując jego poprawność.
    """
    raise NotImplementedError
