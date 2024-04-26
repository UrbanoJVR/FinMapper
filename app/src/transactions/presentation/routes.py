import os
import time

from flask import render_template, session, request, redirect, url_for, current_app
from flask_babel import gettext
from werkzeug.datastructures import CombinedMultiDict

from app.src.transactions import transactions_blueprint
from app.src.transactions.domain.transaction_from_file import TransactionFromFile
from app.src.transactions.infraestructure.file_reader.csv_file_reader import CsvFileReader
from app.src.transactions.infraestructure.file_reader.transactions_file_reader import TransactionsFileReader
from app.src.transactions.presentation.forms import TransactionsFileForm


@transactions_blueprint.route('/transactions', methods=['GET'])
def dashboard():
    return render_template('transactions/transactions_dashboard.html')


@transactions_blueprint.route('/load/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        return render_template('transactions/review_file.html', transactions=session.get('transactions'))

    if request.method == 'POST':
        transanctions = session.get('transactions')
        session.clear()
        return redirect(url_for('transactions_blueprint.load'))


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
    transactions: TransactionFromFile = reader.read_all_transactions()
    session['transactions'] = transactions
    reader.delete_file()


def save_file(data_file):
    _, extension = data_file.filename.split('.')
    filename = f'{int(time.time())}.{extension}'
    data_file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
    return filename
