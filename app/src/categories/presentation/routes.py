from flask import render_template, request, redirect, url_for

from app.src.categories import categories_blueprint
from app.src.categories.application.category_service import CategoryService
from app.src.categories.domain.category import Category
from app.src.categories.infraestructure.category_repository import CategoryRepository
from app.src.categories.presentation.forms import NewCategoryForm

category_service = CategoryService(CategoryRepository())


@categories_blueprint.route('/categories/dashboard', methods=['GET', 'POST'])
def dashboard():
    categories = category_service.get_all_categories()

    if request.method == 'POST':
        create_category(request)
        return redirect(url_for('categories_blueprint.dashboard'))

    return render_template('categories/categories_dashboard.html',
                           categories=categories,
                           new_category_form=NewCategoryForm())


@categories_blueprint.route('/categories/delete/<int:category_id>', methods=['GET'])
def delete(category_id):
    category_service.delete(category_id)
    return '', 204


@categories_blueprint.route('/categories/edit/<int:category_id>', methods=['POST'])
def edit(category_id):
    form = NewCategoryForm(request.form)
    category: Category = Category(
        id=category_id,
        name=form.name.data,
        description=form.description.data
    )
    category_service.update(category)
    return redirect(url_for('categories_blueprint.dashboard'))


def create_category(req):
    new_category_form = NewCategoryForm(req.form)

    if new_category_form.validate_on_submit():
        new_category = Category(
            name=new_category_form.name.data,
            description=new_category_form.description.data
        )
        category_service.save_category(new_category)
        new_category_form.name.data = None
        new_category_form.description.data = None
