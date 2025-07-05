from dataclasses import dataclass
from datetime import date

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetLatestAvailableTransactionYearQuery:
    """Empty query"""
    pass


class GetLatestAvailableTransactionYearHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self) -> int | None:
        years_with_transactions: list[int] = self.transaction_repository.get_years_with_transactions()

        if not years_with_transactions:
            return None

        current_year = date.today().year

        if current_year in years_with_transactions:
            return current_year
        else:
            return max(years_with_transactions)
