from typing import List

from app.src.application.transaction.query.search_transactions_by_month_year_query import \
    SearchTransactionsByMonthYearQuery
from app.src.domain.transaction.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class SearchTransactionsByMonthYearQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, query: SearchTransactionsByMonthYearQuery) -> List[Transaction]:
        return self.transaction_repository.get_by_month_year(query.month, query.year)