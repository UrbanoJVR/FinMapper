import os
import time

from flask import request, current_app, redirect, url_for, render_template, session
from flask_babel import gettext
from werkzeug.datastructures import CombinedMultiDict

from app.file_import import file_import_blueprint
from app.file_import.application.csv_file_reader import CsvFileReader
from app.file_import.forms import TransactionsFileForm
from app.file_import.application.transactions_file_reader import TransactionsFileReader


@file_import_blueprint.route('/load/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        return render_template('file_import/review_file.html', transactions=session.get('transactions'))

    if request.method == 'POST':
        transanctions = session.get('transactions')
        session.clear()
        return redirect(url_for('file_import_blueprint.load'))


@file_import_blueprint.route('/load', methods=['GET', 'POST'])
def load():
    form = TransactionsFileForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'GET':
        return render_template('file_import/load_file.html', form=form, error=None)

    if form.validate_on_submit():
        read_file(save_file(form.file.data))
        return redirect(url_for('file_import_blueprint.review'))
    else:
        error_text = gettext('FileExtensionNotAllowed')
        return render_template('file_import/load_file.html', form=form, error=error_text)


def read_file(filename: str):
    reader: TransactionsFileReader = CsvFileReader(filename)
    transactions = reader.read_all_transactions()
    session['transactions'] = transactions
    reader.delete_file()


def save_file(data_file):
    _, extension = data_file.filename.split('.')
    filename = f'{int(time.time())}.{extension}'
    data_file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
    return filename
