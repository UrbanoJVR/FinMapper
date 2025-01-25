from dataclasses import dataclass, field
from typing import Dict

from app.src.domain.report.category_report import MonthlyData


@dataclass
class YearlyReport:
    year: int
    category_reports: Dict[str, MonthlyData] = field(default_factory=dict)
    #Otros datos que podríamos añadir:
    # numero de transactions sin categorizar
    #año del reporte

    def add_category_report(self, category_name: str, category_report: MonthlyData):
        self.category_reports[category_name] = category_report