from decimal import Decimal

from app.src.domain.category import Category
from app.src.domain.report.category_monthly_data import CategoryMonthlyData
from app.src.domain.report.month import Month
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CalculateMonthlyDataForCategoryQueryHandler:

    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, category: Category, year: int) -> dict[Month, CategoryMonthlyData]:
        monthly_data: dict[Month, CategoryMonthlyData] = {}

        total_cumulative_amount = Decimal("0.00")
        for month in Month:
            transactions = self.transaction_repository.get_by_month_year_and_category_id(month.value, year, category.id)
            total_amount = sum((transaction.amount for transaction in transactions), Decimal("0.00"))
            total_cumulative_amount += total_amount
            cumulative_average = Decimal(total_cumulative_amount / month.value).quantize(Decimal("0.01"))

            monthly_data[month] = CategoryMonthlyData(total_amount, cumulative_average)

        return monthly_data
