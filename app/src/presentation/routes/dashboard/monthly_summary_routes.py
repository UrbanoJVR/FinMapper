from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request
from flask_babel import lazy_gettext

from app.src.infrastructure.repository.transaction_repository import TransactionRepository

monthly_dashboard_blueprint = Blueprint('monthly_dashboard_blueprint', __name__, url_prefix='')

transaction_repository = TransactionRepository()

# Nombres de meses traducibles
MONTH_NAMES = {
    1: lazy_gettext('January'), 2: lazy_gettext('February'), 3: lazy_gettext('March'),
    4: lazy_gettext('April'), 5: lazy_gettext('May'), 6: lazy_gettext('June'),
    7: lazy_gettext('July'), 8: lazy_gettext('August'), 9: lazy_gettext('September'),
    10: lazy_gettext('October'), 11: lazy_gettext('November'), 12: lazy_gettext('December')
}


def get_previous_month(month: int, year: int) -> tuple[int, int]:
    """Obtiene el mes y año anterior"""
    if month == 1:
        return 12, year - 1
    return month - 1, year


def get_next_month(month: int, year: int) -> tuple[int, int]:
    """Obtiene el mes y año siguiente"""
    if month == 12:
        return 1, year + 1
    return month + 1, year


@monthly_dashboard_blueprint.route('/dashboard/<int:year>/<int:month>', methods=['GET'])
def monthly_dashboard(year: int, month: int):
    # Validar que el mes esté entre 1-12
    if month < 1 or month > 12:
        return redirect(url_for('dashboard_blueprint.dashboard_year', year=year))
    
    # Verificar si hay transacciones para este mes
    transactions = transaction_repository.get_by_month_year(month, year)
    
    if not transactions:
        return redirect(url_for('monthly_dashboard_blueprint.empty_monthly_dashboard', year=year, month=month))
    
    month_name = MONTH_NAMES[month]
    previous_month_num, previous_year = get_previous_month(month, year)
    next_month_num, next_year = get_next_month(month, year)
    
    return render_template('dashboard/monthly/monthly_dashboard.html', 
                         selected_year=year, 
                         selected_month=month,
                         month_name=month_name,
                         previous_month=previous_month_num,
                         previous_year=previous_year,
                         next_month=next_month_num,
                         next_year=next_year)


@monthly_dashboard_blueprint.route('/dashboard/<int:year>/<int:month>/empty', methods=['GET'])
def empty_monthly_dashboard(year: int, month: int):
    # Validar que el mes esté entre 1-12
    if month < 1 or month > 12:
        return redirect(url_for('dashboard_blueprint.dashboard_year', year=year))
    
    month_name = MONTH_NAMES[month]
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
