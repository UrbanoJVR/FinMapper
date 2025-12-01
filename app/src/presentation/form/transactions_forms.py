from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, HiddenField

from app.src.shared.date_utils import get_translated_month_names


def get_translated_months():
    """
    Returns a list of tuples (month_number, translated_month_name) for use in SelectField.
    This function uses the shared get_translated_month_names() to avoid code duplication.
    """
    month_names = get_translated_month_names()
    return [(month_num, month_name) for month_num, month_name in month_names.items()]


class MonthYearFilterForm(FlaskForm):
    month = SelectField(choices=get_translated_months())
    year = StringField()
    submit_by_enter = HiddenField(default="false")
    direction = HiddenField(default="no_direction")
