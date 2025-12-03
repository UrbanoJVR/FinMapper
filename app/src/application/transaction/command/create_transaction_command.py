from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from app.src.domain.transaction.vo.transaction_type import TransactionType


@dataclass
class CreateTransactionCommand:
    concept: str
    comments: str
    amount: Decimal
    type: TransactionType
    date: date
    category_id: int = None
