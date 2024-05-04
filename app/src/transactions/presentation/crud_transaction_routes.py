from datetime import datetime

from flask import render_template, request, redirect, url_for

from app.src.categories.application.category_service import CategoryService
from app.src.categories.infraestructure.category_repository import CategoryRepository
from app.src.transactions import transactions_blueprint
from app.src.transactions.application.transaction_service import TransactionService
from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository
from app.src.transactions.presentation.forms import MonthYearFilterForm, TransactionForm

transaction_service = TransactionService(TransactionRepository())
category_service = CategoryService(CategoryRepository())


@transactions_blueprint.route('/transactions', methods=['GET'])
def dashboard():
    return render_template('transactions/transactions_dashboard.html')


@transactions_blueprint.route('/movements', methods=['GET', 'POST'])
def movements_list():
    if request.method == 'GET':
        form = generate_month_year_filter_form_actual_date()
    else:
        form = MonthYearFilterForm(request.form)
        calculate_month_year(form)

    return render_template(
        'transactions/movements_list.html',
        transactions=transaction_service.get_by_month_year(int(form.month.data), int(form.year.data)),
        month_year_filter_form=form
    )


@transactions_blueprint.route('/edit-transaction/<int:transaction_id>', methods=['GET', 'POST'])
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
        return render_template('transactions/edit_transaction.html', form=form)

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
        return redirect(url_for('transactions_blueprint.edit_transaction', transaction_id=transaction.id))


def load_category(category_id):
    if category_id == 'None':  # Verificar si category_id es 'None' como una cadena
        return None
    else:
        return category_service.get_by_id(int(category_id))


@transactions_blueprint.route('/delete-transaction/<int:transaction_id>', methods=['GET'])
def delete_transaction(transaction_id):
    transaction_service.delete(transaction_id)
    return redirect(url_for('transactions_blueprint.movements_list'))


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
    if not form_is_submitted_by_enter_key_pressed(form):
        if form.direction.data == 'previous':
            form.month.data, form.year.data = previous_month(int(form.month.data), int(form.year.data))

        if form.direction.data == 'next':
            form.month.data, form.year.data = next_month(int(form.month.data), int(form.year.data))
