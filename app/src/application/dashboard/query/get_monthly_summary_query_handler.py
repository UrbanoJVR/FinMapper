from dataclasses import dataclass
from decimal import Decimal
from typing import List
from collections import defaultdict

from app.src.domain.transaction.transaction import Transaction
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


@dataclass
class GetMonthlySummaryQuery:
    year: int
    month: int


@dataclass
class CategoryExpense:
    category_id: int | None
    category_name: str
    total_amount: Decimal
    transactions: List[Transaction]


@dataclass
class MonthlySummaryResult:
    year: int
    month: int
    total_expense_amount: Decimal
    category_expenses: List[CategoryExpense]


class GetMonthlySummaryQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, query: GetMonthlySummaryQuery) -> MonthlySummaryResult:
        transactions = self.transaction_repository.get_by_month_year(query.month, query.year)
        
        if not transactions:
            return MonthlySummaryResult(
                year=query.year,
                month=query.month,
                total_expense_amount=Decimal("0.00"),
                category_expenses=[]
            )

        category_groups = defaultdict(list)
        for transaction in transactions:
            category_id = transaction.category.id if transaction.category else None
            category_groups[category_id].append(transaction)

        category_expenses = []
        for category_id, trans_list in category_groups.items():
            category_name = trans_list[0].category.name if trans_list[0].category else "Sin categoría"
            total_amount = sum((t.amount for t in trans_list), Decimal("0.00"))
            
            category_expenses.append(CategoryExpense(
                category_id=category_id,
                category_name=category_name,
                total_amount=total_amount,
                transactions=trans_list
            ))

        category_expenses.sort(key=lambda x: x.total_amount, reverse=True)

        total_expense_amount = sum((ce.total_amount for ce in category_expenses), Decimal("0.00"))

        return MonthlySummaryResult(
            year=query.year,
            month=query.month,
            total_expense_amount=total_expense_amount,
            category_expenses=category_expenses
        )
