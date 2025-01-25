from app.src.application.report.calculate_monthly_data_for_category_query_handler import \
    CalculateMonthlyDataForCategoryQueryHandler
from app.src.domain.report.category_report import MonthlyData
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class CalculateReportDataProcessManager:

    def __init__(self, transaction_repository: TransactionRepository, category_repository: CategoryRepository,
                 monthly_data_query_handler: CalculateMonthlyDataForCategoryQueryHandler):
        self.transaction_repository = transaction_repository
        self.category_repository = category_repository
        self.monthly_data_query_handler = monthly_data_query_handler

    def execute(self, year: int) -> dict[str, MonthlyData]:
        report: dict[str, MonthlyData] = {}

        all_categories = self.category_repository.get_all()
        for category in all_categories:
            category_report = MonthlyData(self.monthly_data_query_handler.execute(category, year))
            report[category.name] = category_report

        return report
