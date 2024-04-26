from datetime import date, datetime


def str_to_date(date_str: str) -> date:
    return datetime.strptime(date_str, '%d/%m/%Y').date()
