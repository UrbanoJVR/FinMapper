from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired


class NewCategoryForm(FlaskForm):
    name = StringField(lazy_gettext('Name'), validators=[DataRequired()], render_kw={"class": "form-control"})
    description = StringField(lazy_gettext('Description'), validators=[DataRequired()], render_kw={"class": "form-control"})
