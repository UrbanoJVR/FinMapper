from datetime import datetime, date

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_babel import gettext

from app.src.application.category.query.get_all_categories_query_handler import GetAllCategoriesQueryHandler
from app.src.application.transaction.command.create_transaction_command_handler import CreateTransactionCommandHandler
from app.src.application.transaction.command.delete_transaction_command_handler import DeleteTransactionCommandHandler
from app.src.application.transaction.command.update_transaction_command_handler import UpdateTransactionCommandHandler
from app.src.application.transaction.query.get_transaction_by_id_query_handler import GetTransactionByIdQueryHandler
from app.src.application.transaction.query.search_transactions_by_month_year_query import \
    SearchTransactionsByMonthYearQuery
from app.src.application.transaction.query.search_transactions_by_month_year_query_handler import \
    SearchTransactionsByMonthYearQueryHandler
from app.src.application.transaction.query.search_uncategorized_transactions_from_last_month_query import \
    SearchUncategorizedTransactionsFromLastMonthQuery
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.application.transaction.command.categorization.categorized_transaction import CategorizedTransaction
from app.src.application.transaction.command.categorization.categorize_transaction_command_handler import \
    CategorizeTransactionCommandHandler
from app.src.application.transaction.service.transaction_service import TransactionService
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from app.src.presentation.form.transactions_forms import MonthYearFilterForm
from app.src.presentation.form.upsert_transaction_form import UpsertTransactionForm, UpsertTransactionFormMapper

transactions_crud_blueprint = Blueprint('transactions_crud_blueprint', __name__, url_prefix='')
transaction_repository = TransactionRepository()
transaction_service = TransactionService(transaction_repository)
category_repository = CategoryRepository()


@transactions_crud_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('transactions/transactions_dashboard.html')


@transactions_crud_blueprint.route('/movements/<int:month>/<int:year>', methods=['GET', 'POST'])
def movements_list(month: int, year: int):
    if request.method == 'GET':
        form = MonthYearFilterForm(month=month, year=year)
        query = SearchTransactionsByMonthYearQuery(month=month, year=year)
        return render_template(
            'transactions/movements_list.html',
            transactions=SearchTransactionsByMonthYearQueryHandler(transaction_repository).execute(query),
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
        transactions = SearchUncategorizedTransactionsFromLastMonthQuery(transaction_repository).execute()
        categories = GetAllCategoriesQueryHandler(category_repository).execute()
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

        CategorizeTransactionCommandHandler(transaction_repository, category_repository).execute(
            categorized_transactions)
        return redirect(url_for('transactions_crud_blueprint.categorize_transaction'))


@transactions_crud_blueprint.route('/edit-transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'GET':
        transaction = GetTransactionByIdQueryHandler(transaction_repository).execute(transaction_id)
        selectable_categories = GetAllCategoriesQueryHandler(category_repository).execute()
        form: UpsertTransactionForm = UpsertTransactionFormMapper().map_from_domain(transaction, selectable_categories)
        return render_template('transactions/upsert_transaction.html', form=form)

    if request.method == 'POST':
        form: UpsertTransactionForm = UpsertTransactionForm(request.form)
        update_transaction_command = UpsertTransactionFormMapper().map_to_update_command(form, transaction_id)
        UpdateTransactionCommandHandler(transaction_repository, category_repository).execute(update_transaction_command)
        flash(gettext('Transaction successfully updated.'), 'success')
        return redirect(url_for('transactions_crud_blueprint.movements_list',
                                month=update_transaction_command.date.month,
                                year=update_transaction_command.date.year))


@transactions_crud_blueprint.route('/transactions/add', methods=['GET', 'POST'])
def create_transaction():
    if request.method == 'GET':
        selectable_categories = GetAllCategoriesQueryHandler(category_repository).execute()
        form = UpsertTransactionFormMapper().initialize(selectable_categories)
        return render_template('transactions/upsert_transaction.html', form=form)

    if request.method == 'POST':
        command = UpsertTransactionFormMapper().map_to_create_command(UpsertTransactionForm(request.form))
        CreateTransactionCommandHandler(transaction_repository, category_repository).execute(command)
        flash(gettext('Transaction successfully created.'), 'success')
        return redirect(url_for('transactions_crud_blueprint.create_transaction'))


@transactions_crud_blueprint.route('/transactions/delete/<int:transaction_id>', methods=['GET'])
def delete_transaction(transaction_id):
    DeleteTransactionCommandHandler(transaction_repository).execute(transaction_id)
    return redirect(request.referrer or url_for('transactions_crud_blueprint.dashboard'))


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
