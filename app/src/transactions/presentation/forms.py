from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext, gettext


class TransactionsFileForm(FlaskForm):
    type = SelectField(lazy_gettext('Type'), choices=[('default', 'DEFAULT'), ('bbva', 'BBVA')])
    file = FileField(lazy_gettext('File'),
                     validators=[DataRequired(),
                                 FileAllowed(['csv'], message='FileExtensionNotAllowed')],
                     render_kw={"class": "form-control"})


class AnotherForm(FlaskForm):
    pass
