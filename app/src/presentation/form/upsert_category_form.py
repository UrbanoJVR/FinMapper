from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.src.application.category.command.create_category_command import CreateCategoryCommand
from app.src.application.category.command.update_category_command import UpdateCategoryCommand


class UpsertCategoryForm(FlaskForm):
    name = StringField(str(lazy_gettext('Name')), validators=[DataRequired()], render_kw={"class": "form-control"})
    description = StringField(str(lazy_gettext('Description')), validators=[DataRequired()],
                              render_kw={"class": "form-control"})

class UpsertCategoryFormMapper:

    @staticmethod
    def map_to_create_command(form: UpsertCategoryForm) -> CreateCategoryCommand:
        return CreateCategoryCommand(form.name.data, form.description.data)

    @staticmethod
    def map_to_update_command(category_id: int, form: UpsertCategoryForm) -> UpdateCategoryCommand:
        return UpdateCategoryCommand(category_id, form.name.data, form.description.data)