from flask import Blueprint, render_template, redirect, url_for

from app.src.application.command_bus import CommandBus
from app.src.application.dashboard.query.get_latest_available_transaction_year_handler import \
    GetLatestAvailableTransactionYearQuery
from app.src.application.query_bus import QueryBus

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__, url_prefix='')

command_bus = CommandBus()
query_bus = QueryBus()

@dashboard_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    latest_year_with_transactions = query_bus.ask(GetLatestAvailableTransactionYearQuery())
    return redirect(url_for('dashboard_blueprint.dashboard_year', year=latest_year_with_transactions))

@dashboard_blueprint.route('/dashboard/<int:year>', methods=['GET'])
def dashboard_year(year: int):
    return render_template('dashboard/dashboard.html')