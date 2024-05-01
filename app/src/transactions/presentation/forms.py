from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext, gettext

months = [(1, lazy_gettext('January')), (2, lazy_gettext('February')), (3, lazy_gettext('March')),
          (4, lazy_gettext('April')), (5, lazy_gettext('May')), (6, lazy_gettext('June')),
          (7, lazy_gettext('July')), (8, lazy_gettext('August')), (9, lazy_gettext('September')),
          (10, lazy_gettext('October')), (11, lazy_gettext('November')), (12, lazy_gettext('December'))]


class TransactionsFileForm(FlaskForm):
    type = SelectField(lazy_gettext('Type'), choices=[('default', 'DEFAULT'), ('bbva', 'BBVA')])
    file = FileField(lazy_gettext('File'),
                     validators=[DataRequired(),
                                 FileAllowed(['csv'], message='FileExtensionNotAllowed')],
                     render_kw={"class": "form-control"})


class MonthYearFilterForm(FlaskForm):
    years = [(year, str(year)) for year in range(2022, 2033)]

    month = SelectField(lazy_gettext('Month'), choices=months)
    year = SelectField(lazy_gettext('Year'), choices=years)
