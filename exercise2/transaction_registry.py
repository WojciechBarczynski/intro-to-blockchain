from simple_cryptography import PrivateKey, hash, PublicKey, sign, verify_signature
from typing import Optional, List
import copy


class Transaction:
    """
    Transakcja zawiera:
    - odbiorcę transakcji (klucz publiczny)
    - hash poprzedniej transakcji
    - własny hash, wyliczony na podstawie dwóch pól powyżej
    - opcjonalny podpis
    """

    recipient: PublicKey
    previous_tx_hash: bytes
    hash: bytes
    signature: Optional[bytes]

    def __init__(self, recipient: PublicKey, previous_tx_hash: bytes):
        """
        Tworzy nową transakcję.
        - recipient - klucz publiczny odbiorcy transakcji
        - previous_tx_hash - hash poprzedniej transakcji, z której zabierane są środki
        """
        self.recipient = recipient
        self.previous_tx_hash = previous_tx_hash

        self.hash = hash(self.recipient.to_bytes() + self.previous_tx_hash)

    def sign(self, private_key: PrivateKey):
        """
        Podpisuje transakcję przy pomocy podanego klucza prywatnego.
        """
        self.signature = sign(private_key, self.hash)

    def __repr__(self):
        return f"Tx(recipient: {self.recipient.to_bytes()[-6:]}.., prev_hash: {self.previous_tx_hash[:6]}..)"


class TransactionRegistry:
    """
    Klasa reprezentująca publiczny rejestr transakcji. Odpowiada za przyjmowanie nowych transakcji i ich
    przechowywanie.
    """

    transactions: List[Transaction]

    def __init__(self, initial_transactions: List[Transaction]):
        self.transactions = copy.copy(initial_transactions)

    def get_transaction(self, tx_hash: bytes) -> Optional[Transaction]:
        for transaction in self.transactions:
            if transaction.hash == tx_hash:
                return transaction
        return None

    def is_transaction_available(self, tx_hash: bytes) -> bool:
        """
        TODO: Sprawdź czy transakcja o podanym hashu istnieje i nie została wykorzystana.
            1.  Sprawdź czy istnieje transakcja o podanym tx_hash, jeśli nie, zwróć False.
            2.  Przeszukaj listę transakcji w poszukiwaniu transakcji, dla której pole
                previous_tx_hash jest równe podanemu w argumencie tx_hash. Jeśli taka transakcja
                istnieje, oznacza to że transakcja o hashu tx_hash zostala już wykorzystana. Zwróć
                False.
            3. Jeśli w poprzednich krokach nic nie zwrócono - transakcja jest dostępna, zwróć True.
        """
        for transaction in self.transactions:
            if transaction.hash == tx_hash or transaction.previous_tx_hash == tx_hash:
                return False
        return True

    def verify_transaction_signature(self, transaction: Transaction) -> bool:
        """
        TODO: Zweryfikuj podpis nowej transakcji.
            1.  Znajdź poprzednią transakcję względem transaction, pole previous_tx_hash z argumentu transaction.
                Jeśli nie istnieje, zwróć False.
            2.  Sprawdź czy dana transakcja została podpisana przez właściciela (klucz publiczny) poprzedniej transakcji.
                Wykorzystaj do tego metodę verify_signature z simple_cryptography.
            Przypomnienie: podpisywany jest hash transakcji.
        """

    def add_transaction(self, transaction: Transaction) -> bool:
        """
        TODO: Dodaj nową transakcję do listy transakcji.
            Przed dodaniem upewnij się, że:
            1.  Poprzednia transakcja jest niewykorzystana.
            2.  Podpis transakcji jest prawidlowy.
            Wykorzystaj do tego dwie metody powyżej.
            Zwróć True jeśli dodanie transakcji przebiegło pomyślnie, False w przeciwnym wypadku.
        """
        raise NotImplementedError()
