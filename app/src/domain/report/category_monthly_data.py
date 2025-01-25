from dataclasses import dataclass
from decimal import Decimal

from app.src.domain.report.month import Month


@dataclass
class CategoryMonthlyData:
    total_amount: Decimal
    cumulative_average: Decimal