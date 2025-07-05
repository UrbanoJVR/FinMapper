from dataclasses import dataclass
from datetime import date

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetActualYearWithTransactionsQuery:
    """Empty query"""
    pass


@dataclass
class GetActualYearWithTransactionsQueryResult:
    year: int | None = None


class GetActualYearWithTransactionsQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self) -> GetActualYearWithTransactionsQueryResult:
        years_with_transactions: list[int] = self.transaction_repository.get_years_with_transactions()

        if not years_with_transactions:
            return GetActualYearWithTransactionsQueryResult(year=None)

        current_year = date.today().year

        if current_year in years_with_transactions:
            return GetActualYearWithTransactionsQueryResult(year=current_year)
        else:
            return GetActualYearWithTransactionsQueryResult(year=max(years_with_transactions))
