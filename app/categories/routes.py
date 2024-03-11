from flask import render_template, request

from app.categories import categories_blueprint
from app.categories.domain.category import Category
from app.categories.forms import NewCategoryForm


def load_categories_from_db():
    total_categories = 14
    categories = []

    for i in range(total_categories):
        name = f"Categoría {i + 1}"
        description = f"Descripción de la Categoría {i + 1}"
        category = Category(name, description)
        categories.append(category)

    return categories


@categories_blueprint.route('/categories/dashboard', methods=['GET', 'POST'])
def dashboard():
    categories = load_categories_from_db()
    new_category_form = NewCategoryForm(request.form)

    if request.method == 'POST':
        form = NewCategoryForm(request.form)
        if form.validate_on_submit():
            new_category = Category(form.name.data, form.description.data)
            categories.append(new_category)
            new_category_form.name.data = None
            new_category_form.description.data = None
            # guardar categoría en base de datos
            print('Se guarda la categoría en base de datos')
            return render_template('categories/categories_dashboard.html',
                                   categories=categories,
                                   new_category_form=new_category_form)

    return render_template('categories/categories_dashboard.html',
                           categories=categories,
                           new_category_form=new_category_form)
