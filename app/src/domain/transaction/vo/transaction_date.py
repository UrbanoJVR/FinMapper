from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class TransactionDate:
    value: date

    def __post_init__(self):
        if self.value is None:
            raise ValueError("value cannot be None")