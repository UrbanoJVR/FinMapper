import decimal
from dataclasses import dataclass


@dataclass
class TransactionFromFile:

    date: str
    concept: str
    amount: str
