from dataclasses import dataclass
from datetime import date

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetLatestAvailableTransactionYearQuery:
    """Empty query"""
    pass


@dataclass
class GetLatestAvailableTransactionYearQueryResult:
    year: int | None = None


class GetLatestAvailableTransactionYearHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self) -> GetLatestAvailableTransactionYearQueryResult:
        years_with_transactions: list[int] = self.transaction_repository.get_years_with_transactions()

        if not years_with_transactions:
            return GetLatestAvailableTransactionYearQueryResult(year=None)

        current_year = date.today().year

        if current_year in years_with_transactions:
            return GetLatestAvailableTransactionYearQueryResult(year=current_year)
        else:
            return GetLatestAvailableTransactionYearQueryResult(year=max(years_with_transactions))
