from dataclasses import dataclass
from typing import List


@dataclass
class CategorizedTransaction:
    transaction_id: int
    category_id: int