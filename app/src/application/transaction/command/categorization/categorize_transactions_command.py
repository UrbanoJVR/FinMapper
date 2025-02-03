from dataclasses import dataclass


@dataclass()
class CategorizedTransaction:
    transaction_id: int
    category_id: int

@dataclass
class CategorizeTransactionsCommand:
    categorized_transactions: list[CategorizedTransaction]