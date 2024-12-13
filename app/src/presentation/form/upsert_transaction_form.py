from datetime import date
from typing import List

from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired

from app.src.application.transaction.command.UpdateTransactionCommand import UpdateTransactionCommand
from app.src.application.transaction.command.create_transaction_command import CreateTransactionCommand
from app.src.domain.category import Category
from app.src.domain.transaction import Transaction


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
    category_id = SelectField(
        str(lazy_gettext('Category'))
    )


class UpsertTransactionFormMapper:

    def initialize(self, selectable_categories: List[Category]) -> UpsertTransactionForm:
        form = UpsertTransactionForm()
        form.date.data = date.today()
        form.category_id.choices = [('None', '')] + [(str(category.id), category.name) for category in
                                                     selectable_categories]

        return form

    def map_from_domain(self, transaction: Transaction, selectable_categories: List[Category]) -> UpsertTransactionForm:
        form = UpsertTransactionForm()
        form.date.data = transaction.transaction_date
        form.amount.data = transaction.amount
        form.concept.data = transaction.concept
        form.category_id.choices = [('None', '')] + [(str(category.id), category.name) for category in
                                                     selectable_categories]
        form.category_id.data = str(transaction.category.id) if transaction.category else 'None'
        form.category_id.selected = form.category_id.data

        return form

    def map_to_create_command(self, form: UpsertTransactionForm) -> CreateTransactionCommand:
        return CreateTransactionCommand(
            date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            category_id=self._get_field_data_if_not_empty(form.category_id),
        )

    def map_to_update_command(self, form: UpsertTransactionForm, transaction_id: int) -> UpdateTransactionCommand:
        return UpdateTransactionCommand(
            transaction_id=transaction_id,
            date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            category_id=self._get_field_data_if_not_empty(form.category_id),
        )

    @staticmethod
    def _get_field_data_if_not_empty(field):
        if not field.data or field.data == 'None':
            return None

        return field.data
