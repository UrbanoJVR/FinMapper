import os
import time

from flask import request, current_app, redirect, url_for, render_template
from flask_babel import gettext
from werkzeug.datastructures import CombinedMultiDict

from app.file_import import file_import_blueprint
from app.file_import.csv_file_reader import CsvFileReader
from app.file_import.forms import TransactionsFileForm
from app.file_import.transactions_file_reader import TransactionsFileReader


@file_import_blueprint.route('/load/data_review', methods=['GET', 'POST'])
def review_file():
    filename = request.args.get('filename')
    reader: TransactionsFileReader = CsvFileReader(filename)
    transactions = reader.read_all_transactions()
    return render_template('file_import/review_file.html', transactions=transactions)


@file_import_blueprint.route('/load', methods=['GET', 'POST'])
def load():
    form = TransactionsFileForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'GET':
        return render_template('file_import/load_file.html', form=form, error=None)

    if form.validate_on_submit():
        filename = save_file(form.file.data)
        return redirect(url_for('file_import_blueprint.review_file', filename=filename))
    else:
        error_text = gettext('FileExtensionNotAllowed')
        return render_template('file_import/load_file.html', form=form, error=error_text)


def save_file(data_file):
    _, extension = data_file.filename.split('.')
    filename = f'{int(time.time())}.{extension}'
    data_file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
    return filename
