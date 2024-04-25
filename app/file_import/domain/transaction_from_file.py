import decimal
from dataclasses import dataclass
from typing import Any


@dataclass
class TransactionFromFile:

    date: Any
    concept: str
    amount: Any
    category_id: int = None
