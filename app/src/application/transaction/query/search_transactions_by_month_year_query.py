from dataclasses import dataclass


@dataclass
class SearchTransactionsByMonthYearQuery:
    month: int
    year: int