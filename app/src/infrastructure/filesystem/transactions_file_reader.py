from abc import ABC, abstractmethod

from app.src.domain.transaction.transaction import Transaction


class TransactionsFileReader(ABC):

    @staticmethod
    @abstractmethod
    def read_all_transactions(file: bytes) -> list[Transaction]:
        pass
