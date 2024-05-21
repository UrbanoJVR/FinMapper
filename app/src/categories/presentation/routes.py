from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_babel import gettext

from app.src.categories.application.category_service import CategoryService
from app.src.categories.domain.category import Category
from app.src.categories.infraestructure.category_repository import CategoryRepository
from app.src.categories.presentation.forms import NewCategoryForm

categories_blueprint = Blueprint('categories_blueprint', __name__, url_prefix='')
category_service = CategoryService(CategoryRepository())


@categories_blueprint.route('/categories/dashboard', methods=['GET', 'POST'])
def categories_dashboard():
    categories = category_service.get_all_categories()

    if request.method == 'POST':
        if create_category(request):
            flash(gettext("Category successfully created!"), "success")
        else:
            flash(gettext("Can't create category"), "warning")
        return redirect(url_for('categories_blueprint.categories_dashboard'))

    return render_template('categories/categories_dashboard.html',
                           categories=categories,
                           new_category_form=NewCategoryForm())


@categories_blueprint.route('/categories/delete/<int:category_id>', methods=['GET'])
def delete(category_id):
    if category_service.is_category_used(category_id):
        flash(gettext("Can't delete used category!"), "warning")
    else:
        category_service.delete(category_id)
        flash(gettext("Category successfully deleted!"), "success")

    return redirect(url_for('categories_blueprint.categories_dashboard'))


@categories_blueprint.route('/categories/edit/<int:category_id>', methods=['POST'])
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
        new_category = Category(
            name=new_category_form.name.data,
            description=new_category_form.description.data
        )
        return category_service.save_category(new_category)
    else:
        return False
