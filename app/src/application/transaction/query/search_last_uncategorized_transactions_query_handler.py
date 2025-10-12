from dataclasses import dataclass
from typing import List

from app.src.domain.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class SearchLastUncategorizedTransactionsQuery:
    """Empty query"""
    pass


from app.src.application.query_bus_registry import query_handler

@query_handler(SearchLastUncategorizedTransactionsQuery)
class SearchLastUncategorizedTransactionsQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository


    def execute(self) -> List[Transaction]:
        last_uncategorized_transaction = self.transaction_repository.get_last_uncategorized()
        if last_uncategorized_transaction is None:
            return []

        return self.transaction_repository.get_uncategorized_by_month_year(
            last_uncategorized_transaction.transaction_date.month,
            last_uncategorized_transaction.transaction_date.year)