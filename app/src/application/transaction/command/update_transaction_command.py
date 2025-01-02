from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class UpdateTransactionCommand:
    transaction_id: int
    concept: str
    amount: Decimal
    date: date
    category_id: int | None