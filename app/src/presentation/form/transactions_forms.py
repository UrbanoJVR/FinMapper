from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import DateField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import DecimalField
from wtforms.fields.simple import StringField, HiddenField
from wtforms.validators import DataRequired

from app.src.application.transaction.command.create_transaction_command import CreateTransactionCommand


def get_translated_months():
    months = [(1, lazy_gettext('January')), (2, lazy_gettext('February')), (3, lazy_gettext('March')),
              (4, lazy_gettext('April')), (5, lazy_gettext('May')), (6, lazy_gettext('June')),
              (7, lazy_gettext('July')), (8, lazy_gettext('August')), (9, lazy_gettext('September')),
              (10, lazy_gettext('October')), (11, lazy_gettext('November')), (12, lazy_gettext('December'))]
    return months


class TransactionsFileForm(FlaskForm):
    type = SelectField(str(lazy_gettext('Type')), choices=[('default', 'DEFAULT'), ('bbva', 'BBVA')])
    file = FileField(str(lazy_gettext('File')),
                     validators=[DataRequired(),
                                 FileAllowed(['csv'], message='FileExtensionNotAllowed')],
                     render_kw={"class": "form-control"})


class MonthYearFilterForm(FlaskForm):
    month = SelectField(choices=get_translated_months())
    year = StringField()
    submit_by_enter = HiddenField(default="false")
    direction = HiddenField(default="no_direction")


class TransactionForm(FlaskForm):
    #TODO extraer a archivo serparado y crear tambien el mapper aparte
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

    def map_to_create_command(self, form: TransactionForm) -> CreateTransactionCommand:
        return CreateTransactionCommand(
            date=form.date.data,
            amount=form.amount.data,
            concept=form.concept.data,
            category_id=self.validate_empty_field(form.category_id),
        )

    @staticmethod
    def validate_empty_field(field):
        if not field.data or field.data == 'None':
            return None

        return field
