import decimal
from dataclasses import dataclass
from datetime import date

from app.src.categories.domain.category import Category


@dataclass
class Transaction:

    transaction_date: date
    amount: decimal.Decimal
    concept: str
    category: Category = None
    id: int = None
