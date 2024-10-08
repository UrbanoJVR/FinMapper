from abc import ABC, abstractmethod


class TransactionsFileReader(ABC):

    @abstractmethod
    def read_all_transactions(self):
        pass

    @abstractmethod
    def delete_file(self):
        pass
