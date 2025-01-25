import decimal
from dataclasses import dataclass
from datetime import date

from app.src.domain.category import Category


@dataclass
class Transaction:

    transaction_date: date
    amount: decimal.Decimal
    concept: str
    comments: str | None = None
    category: Category | None = None
    id: int | None = None
