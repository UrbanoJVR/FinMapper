from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SelectField, FileField
from wtforms.validators import DataRequired

from app.src.domain.file_type import FileType


class TransactionsFileForm(FlaskForm):
    type = SelectField(str(lazy_gettext('Type')), choices=[(ft.name, lazy_gettext(ft.value)) for ft in FileType])
    file = FileField(str(lazy_gettext('File')),
                     validators=[DataRequired(),
                                 # TODO dynamic file allowed extensions list depending on selected file type
                                 FileAllowed(['csv', 'xls', 'xlsx'], message='FileExtensionNotAllowed')],
                     render_kw={"class": "form-control"})