from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_babel import gettext

from app.src.application.category.query.get_all_categories_query_handler import GetAllCategoriesQuery
from app.src.application.command_bus import CommandBus
from app.src.application.query_bus import QueryBus
from app.src.application.transaction.command.categorization.categorize_transactions_command import \
    CategorizeTransactionsCommand, CategorizedTransaction
from app.src.application.transaction.command.delete_transaction_command_handler import DeleteTransactionCommandHandler, \
    DeleteTransactionCommand
from app.src.application.transaction.query.get_transaction_by_id_query_handler import GetTransactionByIdQuery
from app.src.application.transaction.query.search_last_uncategorized_transactions_query_handler import \
    SearchLastUncategorizedTransactionsQuery
from app.src.application.transaction.query.search_transactions_by_month_year_query import \
    SearchTransactionsByMonthYearQuery
from app.src.presentation.form.transactions_forms import MonthYearFilterForm
from app.src.presentation.form.upsert_transaction_form import UpsertTransactionForm, UpsertTransactionFormMapper

transactions_crud_blueprint = Blueprint('transactions_crud_blueprint', __name__, url_prefix='')
command_bus = CommandBus()
query_bus = QueryBus()


@transactions_crud_blueprint.route('/movements/<int:month>/<int:year>', methods=['GET', 'POST'])
def movements_list(month: int, year: int):
    if request.method == 'GET':
        form = MonthYearFilterForm(month=month, year=year)
        transactions = query_bus.ask(SearchTransactionsByMonthYearQuery(month, year))
        return render_template(
            'transactions/movements_list.html',
            transactions=transactions,
            month_year_filter_form=form
        )

    if request.method == 'POST':
        month, year = calculate_month_year(MonthYearFilterForm(request.form))
        return redirect(url_for('transactions_crud_blueprint.movements_list', month=month, year=year))


@transactions_crud_blueprint.route('/movements', methods=['GET'])
def movements():
    now = datetime.now()
    return redirect(url_for('transactions_crud_blueprint.movements_list', month=now.month, year=now.year))


@transactions_crud_blueprint.route('/transactions/categorize', methods=['GET', 'POST'])
def categorize_transaction():
    if request.method == 'GET':
        transactions = query_bus.ask(SearchLastUncategorizedTransactionsQuery())
        categories = query_bus.ask(GetAllCategoriesQuery())
        return render_template('transactions/categorize_transactions.html',
                               transactions=transactions,
                               categories=categories)

    if request.method == 'POST':
        categorized_transactions = []
        for transaction_id, category_id in request.form.items():
            if category_id:
                categorized_transactions.append(
                    CategorizedTransaction(transaction_id=int(transaction_id),
                                           category_id=int(category_id)))

        command_bus.execute(CategorizeTransactionsCommand(categorized_transactions))
        return redirect(url_for('transactions_crud_blueprint.categorize_transaction'))


@transactions_crud_blueprint.route('/edit-transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'GET':
        transaction = query_bus.ask(GetTransactionByIdQuery(transaction_id))
        selectable_categories = query_bus.ask(GetAllCategoriesQuery())
        form: UpsertTransactionForm = UpsertTransactionFormMapper().map_from_domain(transaction, selectable_categories)
        return render_template('transactions/upsert_transaction.html', form=form)

    if request.method == 'POST':
        form: UpsertTransactionForm = UpsertTransactionForm(request.form)
        update_transaction_command = UpsertTransactionFormMapper().map_to_update_command(form, transaction_id)
        command_bus.execute(update_transaction_command)
        flash(gettext('Transaction successfully updated.'), 'success')
        return redirect(url_for('transactions_crud_blueprint.movements_list',
                                month=update_transaction_command.date.month,
                                year=update_transaction_command.date.year))


@transactions_crud_blueprint.route('/transactions/add', methods=['GET', 'POST'])
def create_transaction():
    if request.method == 'GET':
        selectable_categories = query_bus.ask(GetAllCategoriesQuery())
        form = UpsertTransactionFormMapper().initialize(selectable_categories)
        return render_template('transactions/upsert_transaction.html', form=form)

    if request.method == 'POST':
        command = UpsertTransactionFormMapper().map_to_create_command(UpsertTransactionForm(request.form))
        command_bus.execute(command)
        flash(gettext('Transaction successfully created.'), 'success')
        return redirect(url_for('transactions_crud_blueprint.create_transaction'))


@transactions_crud_blueprint.route('/transactions/delete/<int:transaction_id>', methods=['GET'])
def delete_transaction(transaction_id):
    command_bus.execute(DeleteTransactionCommand(transaction_id))
    return redirect(request.referrer or url_for('dashboard_blueprint.report'))


def generate_month_year_filter_form_actual_date():
    now = datetime.now()
    return MonthYearFilterForm(month=now.month, year=now.year)


def previous_month(month, year):
    if month == 1:
        return str(12), str(year - 1)
    else:
        return str(month - 1), str(year)


def next_month(month, year):
    if month == 12:
        return str(1), str(year + 1)
    else:
        return str(month + 1), str(year)


def form_is_submitted_by_enter_key_pressed(form: MonthYearFilterForm) -> bool:
    if form.submit_by_enter.data == 'true':
        return True

    return False


def calculate_month_year(form: MonthYearFilterForm):
    if form_is_submitted_by_enter_key_pressed(form):
        return form.month.data, form.year.data

    if form.direction.data == 'previous':
        return previous_month(int(form.month.data), int(form.year.data))

    if form.direction.data == 'next':
        return next_month(int(form.month.data), int(form.year.data))

    return form.month.data, form.year.data
