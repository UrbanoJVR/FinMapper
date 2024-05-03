import os
import time
from datetime import datetime
from typing import List

from flask import render_template, session, request, redirect, url_for, current_app
from flask_babel import gettext
from werkzeug.datastructures import CombinedMultiDict

from app.src.categories.application.category_service import CategoryService
from app.src.categories.domain.category import Category
from app.src.categories.infraestructure.category_repository import CategoryRepository
from app.src.transactions import transactions_blueprint
from app.src.transactions.application.transaction_service import TransactionService
from app.src.transactions.domain.transaction import Transaction
from app.src.transactions.domain.transaction_from_file import TransactionFromFile
from app.src.transactions.infraestructure.file_reader.csv_file_reader import CsvFileReader
from app.src.transactions.infraestructure.file_reader.transactions_file_reader import TransactionsFileReader
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository
from app.src.transactions.presentation.forms import TransactionsFileForm, MonthYearFilterForm, TransactionForm
from app.src.transactions.presentation.transaction_from_file_mapper import map_to_entity_list

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
        form.category.choices = [('None', '')] + [(str(category.id), category.name) for category in category_service.get_all_categories()]
        form.category.selected = form.category.data
        form.category.data = str(transaction.category.id) if transaction.category else 'None'
        return render_template('transactions/edit_transaction.html', form=form)

    if request.method == 'POST':
        form: TransactionForm = TransactionForm(request.form)
        transaction = Transaction(
            id=transaction_id,
            transaction_date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            category=category_service.get_by_id(int(str(form.category.data)))
        )
        transaction_service.update(transaction)
        return render_template('transactions/edit_transaction.html', form=TransactionForm())


@transactions_blueprint.route('/delete-transaction/<int:transaction_id>', methods=['GET', 'POST'])
def delete_transaction(transaction_id):
    if request.method == 'POST':
        # Aquí eliminas el movimiento con el ID proporcionado
        return redirect(url_for('transactions.movements_list'))
    else:
        # Aquí puedes renderizar un template de confirmación de eliminación
        return None


@transactions_blueprint.route('/load/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        return render_template('transactions/review_file.html', transactions=session.get('transactions'))

    if request.method == 'POST':
        transaction_service.save_transactions(
            map_to_entity_list(session.get('transactions'))
        )
        session.pop('transactions')
        return redirect(url_for('transactions_blueprint.load_transactions_file'))


@transactions_blueprint.route('/load', methods=['GET', 'POST'])
def load_transactions_file():
    form = TransactionsFileForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'GET':
        return render_template('transactions/load_file.html', form=form, error=None)

    if form.validate_on_submit():
        read_file(save_file(form.file.data))
        return redirect(url_for('transactions_blueprint.review'))
    else:
        error_text = gettext('FileExtensionNotAllowed')
        return render_template('transactions/load_file.html', form=form, error=error_text)


def read_file(filename: str):
    reader: TransactionsFileReader = CsvFileReader(filename)
    transactions: List[TransactionFromFile] = reader.read_all_transactions()
    session['transactions'] = transactions
    reader.delete_file()


def save_file(data_file):
    _, extension = data_file.filename.split('.')
    filename = f'{int(time.time())}.{extension}'
    data_file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
    return filename


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
