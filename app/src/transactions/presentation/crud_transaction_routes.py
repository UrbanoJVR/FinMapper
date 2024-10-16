from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_babel import gettext

from app.src.categories.application.category_service import CategoryService
from app.src.categories.infraestructure.category_repository import CategoryRepository
from app.src.transactions.application.categorization.categorize_transaction_command import CategorizedTransaction
from app.src.transactions.application.categorization.categorize_transaction_command_handler import \
    CategorizeTransactionCommandHandler
from app.src.transactions.application.transaction_service import TransactionService
from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository
from app.src.transactions.presentation.forms import MonthYearFilterForm, TransactionForm

transactions_crud_blueprint = Blueprint('transactions_crud_blueprint', __name__, url_prefix='')
transaction_repository = TransactionRepository()
transaction_service = TransactionService(transaction_repository)
category_repository = CategoryRepository()
category_service = CategoryService(category_repository)


@transactions_crud_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('transactions/transactions_dashboard.html')


@transactions_crud_blueprint.route('/movements/<int:month>/<int:year>', methods=['GET', 'POST'])
def movements_list(month: int, year: int):
    if request.method == 'GET':
        form = MonthYearFilterForm(month=month, year=year)
        return render_template(
            'transactions/movements_list.html',
            transactions=transaction_service.get_by_month_year(int(form.month.data), int(form.year.data)),
            month_year_filter_form=form
        )

    if request.method == 'POST':
        month, year = calculate_month_year(MonthYearFilterForm(request.form))
        return redirect(url_for('transactions_crud_blueprint.movements_list', month=month, year=year))


@transactions_crud_blueprint.route('/movements', methods=['GET', 'POST'])
def movements():
    now = datetime.now()
    return redirect(url_for('transactions_crud_blueprint.movements_list', month=now.month, year=now.year))


@transactions_crud_blueprint.route('/transactions/categorize', methods=['GET', 'POST'])
def categorize_transaction():
    if request.method == 'GET':
        transactions = transaction_service.get_last_month_uncategorized()
        categories = category_service.get_all_categories()
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

        CategorizeTransactionCommandHandler(categorized_transactions, transaction_repository, category_repository).execute()
        return redirect(url_for('transactions_crud_blueprint.categorize_transaction'))


@transactions_crud_blueprint.route('/edit-transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'GET':
        transaction = transaction_service.get_by_id(transaction_id)
        form = TransactionForm()
        form.date.data = transaction.transaction_date
        form.amount.data = transaction.amount
        form.concept.data = transaction.concept
        form.category_id.choices = [('None', '')] + [(str(category.id), category.name) for category in
                                                     category_service.get_all_categories()]
        form.category_id.data = str(transaction.category.id) if transaction.category else 'None'
        form.category_id.selected = form.category_id.data
        return render_template('transactions/upsert_transaction.html', form=form)

    if request.method == 'POST':
        form: TransactionForm = TransactionForm(request.form)
        transaction = Transaction(
            id=transaction_id,
            transaction_date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            category=load_category(form.category_id.data)
        )
        transaction_service.update(transaction)
        flash(gettext('Transaction successfully updated.'), 'success')
        return redirect(url_for('transactions_crud_blueprint.movements_list',
                                month=transaction.transaction_date.month,
                                year=transaction.transaction_date.year))


@transactions_crud_blueprint.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        form = TransactionForm()
        form.date.data = datetime.now()
        form.category_id.choices = [('None', '')] + [(str(category.id), category.name) for category in
                                                     category_service.get_all_categories()]
        return render_template('transactions/upsert_transaction.html', form=form)

    if request.method == 'POST':
        form = TransactionForm(request.form)
        transaction = Transaction(
            transaction_date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            category=load_category(form.category_id.data)
        )
        transaction_service.create(transaction)
        flash(gettext('Transaction successfully created.'), 'success')
        return redirect(url_for('transactions_crud_blueprint.add_transaction'))


def load_category(category_id):
    if category_id == 'None':
        return None
    else:
        return category_service.get_by_id(int(category_id))


@transactions_crud_blueprint.route('/transactions/delete/<int:transaction_id>', methods=['GET'])
def delete_transaction(transaction_id):
    transaction_service.delete(transaction_id)
    return redirect(request.referrer or url_for('home'))


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
