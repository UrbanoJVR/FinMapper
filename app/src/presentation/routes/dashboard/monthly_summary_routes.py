from flask import Blueprint, render_template, redirect, url_for

from app.src.application.dashboard.query.get_monthly_summary_query_handler import GetMonthlySummaryQuery
from app.src.application.query_bus import QueryBus
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from app.src.shared.date_utils import get_translated_month_names

monthly_dashboard_blueprint = Blueprint('monthly_dashboard_blueprint', __name__, url_prefix='')

transaction_repository = TransactionRepository()
query_bus = QueryBus()


def get_previous_month(month: int, year: int) -> tuple[int, int]:
    """Get the previous month and year"""
    if month == 1:
        return 12, year - 1
    return month - 1, year


def get_next_month(month: int, year: int) -> tuple[int, int]:
    """Get the next month and year"""
    if month == 12:
        return 1, year + 1
    return month + 1, year


@monthly_dashboard_blueprint.route('/dashboard/<int:year>/<int:month>', methods=['GET'])
def monthly_dashboard(year: int, month: int):
    # Validate that the month is between 1-12
    if month < 1 or month > 12:
        return redirect(url_for('dashboard_blueprint.dashboard_year', year=year))

    # Check if there are transactions for this month
    transactions = transaction_repository.get_by_month_year(month, year)

    if not transactions:
        return redirect(url_for('monthly_dashboard_blueprint.empty_monthly_dashboard', year=year, month=month))

    monthly_summary = query_bus.ask(GetMonthlySummaryQuery(year, month))
    month_names = get_translated_month_names()
    month_name = month_names[month]
    previous_month_num, previous_year = get_previous_month(month, year)
    next_month_num, next_year = get_next_month(month, year)

    return render_template('dashboard/monthly/monthly_dashboard.html',
                           selected_year=year,
                           selected_month=month,
                           month_name=month_name,
                           monthly_summary=monthly_summary,
                           previous_month=previous_month_num,
                           previous_year=previous_year,
                           next_month=next_month_num,
                           next_year=next_year)


@monthly_dashboard_blueprint.route('/dashboard/<int:year>/<int:month>/empty', methods=['GET'])
def empty_monthly_dashboard(year: int, month: int):
    # Validate that the month is between 1-12
    if month < 1 or month > 12:
        return redirect(url_for('dashboard_blueprint.dashboard_year', year=year))

    month_names = get_translated_month_names()
    month_name = month_names[month]
    previous_month_num, previous_year = get_previous_month(month, year)
    next_month_num, next_year = get_next_month(month, year)

    return render_template('dashboard/monthly/empty_monthly_dashboard.html',
                           selected_year=year,
                           selected_month=month,
                           month_name=month_name,
                           previous_month=previous_month_num,
                           previous_year=previous_year,
                           next_month=next_month_num,
                           next_year=next_year)
