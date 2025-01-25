from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict
from app.src.domain.report.category_monthly_data import CategoryMonthlyData
from app.src.domain.report.month import Month

@dataclass
class MonthlyData:
    value: Dict[Month, CategoryMonthlyData] = field(default_factory=lambda: {
        month: CategoryMonthlyData(total_amount=Decimal("0.00"), cumulative_average=Decimal("0.00"))
        for month in Month
    })

    def total_annual_amount(self) -> Decimal:
        """Calculates the total amount spent in this category for the entire year."""
        return sum((data.total_amount for data in self.value.values()), Decimal('0.00'))
