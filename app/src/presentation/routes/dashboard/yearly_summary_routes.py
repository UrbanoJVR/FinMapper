from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request

from app.src.application.command_bus import CommandBus
from app.src.application.dashboard.query.get_latest_available_transaction_year_handler import \
    GetLatestAvailableTransactionYearQuery
from app.src.application.dashboard.query.get_dashboard_summary_query_handler import \
    GetDashboardSummaryQuery, DashboardSummaryResult
from app.src.application.query_bus import QueryBus
from app.src.infrastructure.repository.transaction_repository import TransactionRepository

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__, url_prefix='')

command_bus = CommandBus()
query_bus = QueryBus()
transaction_repository = TransactionRepository()


@dashboard_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    latest_year_with_transactions = query_bus.ask(GetLatestAvailableTransactionYearQuery())

    if latest_year_with_transactions is None:
        return redirect(url_for('dashboard_blueprint.empty_dashboard'))

    return redirect(url_for('dashboard_blueprint.dashboard_year', year=latest_year_with_transactions))


@dashboard_blueprint.route('/dashboard/<int:year>', methods=['GET'])
def dashboard_year(year: int):
    years_with_transactions = transaction_repository.get_years_with_transactions()

    if year not in years_with_transactions:
        return redirect(url_for('dashboard_blueprint.empty_dashboard', year=year))

    dashboard_summary: DashboardSummaryResult = query_bus.ask(GetDashboardSummaryQuery(year))
    return render_template('dashboard/yearly/dashboard.html', selected_year=year, dashboard_summary=dashboard_summary)


@dashboard_blueprint.route('/dashboard/empty', methods=['GET'])
def empty_dashboard():
    year = request.args.get('year', type=int)
    if year is None:
        year = datetime.now().year
    return render_template('dashboard/yearly/empty_dashboard.html', selected_year=year)
