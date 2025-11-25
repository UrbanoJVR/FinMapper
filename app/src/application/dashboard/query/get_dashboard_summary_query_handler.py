from dataclasses import dataclass
from decimal import Decimal

from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetDashboardSummaryQuery:
    year: int


@dataclass
class DashboardSummaryResult:
    year: int
    total_expense_amount: Decimal
    average_expense_amount: Decimal
    total_transactions_count: int
    months_with_data: set[int]


class GetDashboardSummaryQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, query: GetDashboardSummaryQuery) -> DashboardSummaryResult:
        transactions = self.transaction_repository.get_by_year(query.year)
        
        if not transactions:
            return DashboardSummaryResult(
                year=query.year,
                total_expense_amount=Decimal("0.00"),
                average_expense_amount=Decimal("0.00"),
                total_transactions_count=0,
                months_with_data=set()
            )

        total_expense_amount = sum(
            (transaction.amount for transaction in transactions), 
            Decimal("0.00")
        )

        distinct_months = set(transaction.transaction_date.value.month for transaction in transactions)
        months_count = len(distinct_months)
        average_expense_amount = (
            total_expense_amount / months_count if months_count > 0 else Decimal("0.00")
        )
        
        total_transactions_count = len(transactions)
        
        return DashboardSummaryResult(
            year=query.year,
            total_expense_amount=total_expense_amount,
            average_expense_amount=average_expense_amount,
            total_transactions_count=total_transactions_count,
            months_with_data=distinct_months
        )
