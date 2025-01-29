from flask import request, render_template, session, redirect, url_for, Blueprint, flash
from flask_babel import gettext
from werkzeug.datastructures import CombinedMultiDict

from app.src.application.transaction.command.create_multiple_transactions_command_handler import \
    CreateMultipleTransactionsCommandHandler
from app.src.application.transaction.command.read_transactions_from_file_command import ReadTransactionsFromFileCommand
from app.src.application.transaction.command.read_transactions_from_file_command_handler import \
    ReadTransactionsFromFileCommandHandler
from app.src.application.transaction.query.get_transactions_in_memory_query_handler import \
    GetTransactionsInMemoryQueryHandler
from app.src.domain.file_type import FileType
from app.src.domain.transaction import Transaction
from app.src.infrastructure.filesystem.file_reader_factory import FileReaderFactory
from app.src.infrastructure.in_memory.transaction_memory_repository import TransactionMemoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from app.src.presentation.form.transactions_file_form import TransactionsFileForm

transactions_file_blueprint = Blueprint('transactions_file_blueprint', __name__, url_prefix='')


@transactions_file_blueprint.route('/load/review', methods=['GET', 'POST'])
def review_file():
    transactions: list[Transaction] = GetTransactionsInMemoryQueryHandler(TransactionMemoryRepository()).execute()

    if request.method == 'GET':
        return render_template('transactions/review_file.html', transactions=transactions)

    if request.method == 'POST':
        CreateMultipleTransactionsCommandHandler(TransactionRepository()).execute(transactions)
        flash(gettext('Transactions saved successfully!'), 'success')
        session.pop('transactions')
        return redirect(url_for('transactions_file_blueprint.load_transactions_file'))


@transactions_file_blueprint.route('/load', methods=['GET', 'POST'])
def load_transactions_file():
    form = TransactionsFileForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'GET':
        return render_template('transactions/load_file.html', form=form)

    if form.validate_on_submit():
        command = ReadTransactionsFromFileCommand(form.file.data, FileType.__getitem__(form.type.data))
        handler = ReadTransactionsFromFileCommandHandler(TransactionMemoryRepository(), FileReaderFactory())
        handler.execute(command)
        return redirect(url_for('transactions_file_blueprint.review_file'))
    else:
        flash(gettext("FileExtensionNotAllowed"), 'error')
        return render_template('transactions/load_file.html', form=form)
