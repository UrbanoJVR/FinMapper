from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class TransactionAmount:
    value: Decimal

    def __post_init__(self):
        if self.value is None:
            raise ValueError("value cannot be None")