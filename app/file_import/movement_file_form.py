from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l


class MovementFileForm(FlaskForm):
    type = SelectField(_l('Type'), choices=[('default', 'DEFAULT'), ('bbva', 'BBVA')])
    file = FileField(_l('File'), render_kw={"class": "form-control"})
