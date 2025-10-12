from dataclasses import dataclass
from decimal import Decimal

from app.src.application.query_bus_registry import query_handler
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetTotalExpensesByYearQuery:
    year: int


@query_handler(GetTotalExpensesByYearQuery)
class GetTotalExpensesByYearQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, query: GetTotalExpensesByYearQuery) -> Decimal:
        transactions = self.transaction_repository.get_by_year(query.year)
        return sum((transaction.amount for transaction in transactions), Decimal("0.00"))
