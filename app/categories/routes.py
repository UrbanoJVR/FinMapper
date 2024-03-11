from flask import render_template

from app.categories import categories_blueprint


@categories_blueprint.route('/categories/dashboard')
def dashboard():
    return render_template('categories/categories_dashboard.html')
