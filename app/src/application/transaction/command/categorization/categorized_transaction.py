from dataclasses import dataclass


@dataclass
class CategorizedTransaction:
    transaction_id: int
    category_id: int
