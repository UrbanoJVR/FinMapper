import os
from datetime import datetime
from typing import List

from flask import request, render_template, session, redirect, url_for, current_app, Blueprint, flash
from flask_babel import gettext
from werkzeug.datastructures import CombinedMultiDict

from app.src.transactions.application.transaction_service import TransactionService
from app.src.transactions.domain.transaction_from_file import TransactionFromFile
from app.src.transactions.infraestructure.file_reader.csv_file_reader import CsvFileReader
from app.src.transactions.infraestructure.file_reader.transactions_file_reader import TransactionsFileReader
from app.src.transactions.infraestructure.repository.transaction_repository import TransactionRepository
from app.src.transactions.presentation.forms import TransactionsFileForm
from app.src.transactions.presentation.transaction_from_file_mapper import map_to_entity_list

transactions_file_blueprint = Blueprint('transactions_file_blueprint', __name__, url_prefix='')
transaction_service = TransactionService(TransactionRepository())


@transactions_file_blueprint.route('/load/review', methods=['GET', 'POST'])
def review_file():
    if request.method == 'GET':
        return render_template('transactions/review_file.html', transactions=session.get('transactions'))

    if request.method == 'POST':
        transaction_service.save_transactions(
            map_to_entity_list(session.get('transactions'))
        )
        flash(gettext('Transactions saved successfully!'), 'success')
        session.pop('transactions')
        return redirect(url_for('transactions_file_blueprint.load_transactions_file'))


@transactions_file_blueprint.route('/load', methods=['GET', 'POST'])
def load_transactions_file():
    form = TransactionsFileForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'GET':
        return render_template('transactions/load_file.html', form=form, error=None)

    if form.validate_on_submit():
        read_file(save_file(form.file.data))
        return redirect(url_for('transactions_file_blueprint.review_file'))
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
    filename = f'{datetime.now().timestamp()}.{extension}'
    data_file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
    return filename
