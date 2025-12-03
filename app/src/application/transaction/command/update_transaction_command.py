from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.src.domain.transaction.vo.transaction_type import TransactionType


@dataclass
class UpdateTransactionCommand:
    transaction_id: int
    concept: str
    comments: str
    amount: Decimal
    date: date
    type: TransactionType
    category_id: int | None
