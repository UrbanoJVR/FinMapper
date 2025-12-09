from datetime import date
from typing import List

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired

from app.src.application.transaction.command.update_transaction_command import UpdateTransactionCommand
from app.src.application.transaction.command.create_transaction_command import CreateTransactionCommand
from app.src.domain.category import Category
from app.src.domain.transaction.transaction import Transaction
from app.src.domain.transaction.vo.transaction_type import TransactionType


class UpsertTransactionForm(FlaskForm):
    date: DateField = DateField(
        str(lazy_gettext('Date')),
        validators=[DataRequired(message=str(lazy_gettext('Date required')))]
    )
    amount = DecimalField(
        str(lazy_gettext('Amount')),
        validators=[DataRequired(message=str(lazy_gettext('Amount required')))]
    )
    concept = StringField(
        str(lazy_gettext('Concept')),
        validators=[DataRequired(message=str(lazy_gettext('Concept required')))]
    )
    comments = StringField(
        str(lazy_gettext('Comments')),
    )
    category_id = SelectField(
        str(lazy_gettext('Category'))
    )
    type = RadioField(
        str(lazy_gettext('Transaction Type')),
        choices=[
            (TransactionType.EXPENSE.value, str(lazy_gettext('Expense'))),
            (TransactionType.INCOME.value, str(lazy_gettext('Income')))
        ],
        default=TransactionType.EXPENSE.value
    )


class UpsertTransactionFormMapper:

    def initialize(self, selectable_categories: List[Category]) -> UpsertTransactionForm:
        form = UpsertTransactionForm()
        form.date.data = date.today()
        form.category_id.choices = [('None', '')] + [(str(category.id), category.name) for category in
                                                     selectable_categories]
        form.type.data = TransactionType.EXPENSE.value

        return form

    def map_from_domain(self, transaction: Transaction, selectable_categories: List[Category]) -> UpsertTransactionForm:
        form = UpsertTransactionForm()
        form.date.data = transaction.transaction_date.value
        form.amount.data = transaction.amount.value
        form.concept.data = transaction.concept
        form.comments.data = transaction.comments
        form.category_id.choices = [('None', '')] + [(str(category.id), category.name) for category in
                                                     selectable_categories]
        form.category_id.data = str(transaction.category.id) if transaction.category else 'None'
        form.category_id.selected = form.category_id.data
        form.type.data = transaction.type.value

        return form

    def map_to_create_command(self, form: UpsertTransactionForm) -> CreateTransactionCommand:
        transaction_type = TransactionType(form.type.data) if form.type.data else TransactionType.EXPENSE
        return CreateTransactionCommand(
            date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            comments=form.comments.data,
            category_id=self._get_field_data_if_not_empty(form.category_id),
            type=transaction_type,
        )

    def map_to_update_command(self, form: UpsertTransactionForm, transaction_id: int) -> UpdateTransactionCommand:
        transaction_type = TransactionType(form.type.data) if form.type.data else TransactionType.EXPENSE
        return UpdateTransactionCommand(
            transaction_id=transaction_id,
            date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            comments=form.comments.data,
            category_id=self._get_field_data_if_not_empty(form.category_id),
            type=transaction_type,
        )

    @staticmethod
    def _get_field_data_if_not_empty(field):
        if not field.data or field.data == 'None':
            return None

        return field.data
