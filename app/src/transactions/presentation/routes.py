import os
import time
from datetime import datetime
from typing import List

from flask import render_template, session, request, redirect, url_for, current_app
from flask_babel import gettext
from werkzeug.datastructures import CombinedMultiDict

from app.src.transactions import transactions_blueprint
from app.src.transactions.application.transaction_service import TransactionService
from app.src.transactions.domain.transaction_from_file import TransactionFromFile
from app.src.transactions.infraestructure.file_reader.csv_file_reader import CsvFileReader
from app.src.transactions.infraestructure.file_reader.transactions_file_reader import TransactionsFileReader
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository
from app.src.transactions.presentation.forms import TransactionsFileForm, MonthYearFilterForm
from app.src.transactions.presentation.transaction_from_file_mapper import map_to_entity_list

transaction_service = TransactionService(TransactionRepository())


@transactions_blueprint.route('/transactions', methods=['GET'])
def dashboard():
    return render_template('transactions/transactions_dashboard.html')


@transactions_blueprint.route('/movements', methods=['GET', 'POST'])
def movements_list():
    if request.method == 'GET':
        form = generate_month_year_filter_form_actual_date()
    else:
        form = MonthYearFilterForm(request.form)

        if request.form.get('direction') == 'previous':
            form.month.data, form.year.data = previous_month(int(form.month.data), int(form.year.data))

        if request.form.get('direction') == 'next':
            form.month.data, form.year.data = next_month(int(form.month.data), int(form.year.data))

    return render_template(
        'transactions/movements_list.html',
        transactions=transaction_service.get_by_month_year(form.month.data, form.year.data),
        month_year_filter_form=form
    )


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
