from dataclasses import dataclass
from decimal import Decimal

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetAverageMonthlySpendingByYearQuery:
    year: int


class GetAverageMonthlySpendingByYearQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, query: GetAverageMonthlySpendingByYearQuery) -> Decimal:
        transactions = self.transaction_repository.get_by_year(query.year)
        
        if not transactions:
            return Decimal("0.00")
        
        # Extract distinct months from transactions
        distinct_months = set()
        for transaction in transactions:
            distinct_months.add(transaction.transaction_date.month)
        
        # Calculate total expenses
        total_expenses = sum((transaction.amount for transaction in transactions), Decimal("0.00"))
        
        # Calculate average (total / number of distinct months)
        months_count = len(distinct_months)
        if months_count == 0:
            return Decimal("0.00")
        
        return total_expenses / months_count

