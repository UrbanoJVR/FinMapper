from flask import render_template, request, redirect, url_for

from app.categories import categories_blueprint
from app.categories.application.category_service import CategoryService
from app.categories.domain.category import Category
from app.categories.forms import NewCategoryForm
from app.categories.infraestructure.category_repository import CategoryRepository

category_service = CategoryService(CategoryRepository())


@categories_blueprint.route('/categories/dashboard', methods=['GET', 'POST'])
def dashboard():
    categories = category_service.get_all_categories()
    new_category_form = NewCategoryForm(request.form)

    if request.method == 'POST':
        if new_category_form.validate_on_submit():
            new_category = Category(
                name=new_category_form.name.data,
                description=new_category_form.description.data
            )
            category_service.save_category(new_category)
            new_category_form.name.data = None
            new_category_form.description.data = None
            return redirect(url_for('categories_blueprint.dashboard'))

    return render_template('categories/categories_dashboard.html',
                           categories=categories,
                           new_category_form=new_category_form)
