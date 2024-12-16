from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_babel import gettext

from app.src.application.category.command.create_category_command import CreateCategoryCommand
from app.src.application.category.command.create_category_command_handler import CreateCategoryCommandHandler
from app.src.application.category.query.get_all_categories_query_handler import GetAllCategoriesQueryHandler
from app.src.application.category.service.category_service import CategoryService
from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.presentation.form.category_forms import NewCategoryForm

categories_blueprint = Blueprint('categories_blueprint', __name__, url_prefix='/categories')
category_repository = CategoryRepository()
category_service = CategoryService(category_repository)


@categories_blueprint.route('/dashboard', methods=['GET', 'POST'])
def categories_dashboard():
    categories = GetAllCategoriesQueryHandler(category_repository).execute()

    if request.method == 'POST':
        if create_category(request):
            flash(gettext("Category successfully created!"), "success")
        else:
            flash(gettext("Can't create category"), "warning")
        return redirect(url_for('categories_blueprint.categories_dashboard'))

    return render_template('categories/categories_dashboard.html',
                           categories=categories,
                           new_category_form=NewCategoryForm())


@categories_blueprint.route('/delete/<int:category_id>', methods=['GET'])
def delete(category_id):
    if category_service.is_category_used(category_id):
        flash(gettext("Can't delete used category!"), "warning")
    else:
        category_service.delete(category_id)
        flash(gettext("Category successfully deleted!"), "success")

    return redirect(url_for('categories_blueprint.categories_dashboard'))


@categories_blueprint.route('/edit/<int:category_id>', methods=['POST'])
def edit(category_id):
    form = NewCategoryForm(request.form)
    category: Category = Category(
        id=category_id,
        name=form.name.data,
        description=form.description.data
    )
    category_service.update(category)
    return redirect(url_for('categories_blueprint.categories_dashboard'))


def create_category(req) -> bool:
    new_category_form = NewCategoryForm(req.form)

    if new_category_form.validate_on_submit():
        create_category_command = CreateCategoryCommand(
            name=new_category_form.name.data,
            description=new_category_form.description.data
        )
        handler = CreateCategoryCommandHandler(category_repository)
        return handler.execute(create_category_command)
    else:
        return False
