from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_babel import gettext

from app.src.application.category.command.create_category_command import CreateCategoryCommand
from app.src.application.category.command.create_category_command_handler import CreateCategoryCommandHandler
from app.src.application.category.command.delete_category_process_manager import DeleteCategoryProcessManager
from app.src.application.category.command.update_category_command import UpdateCategoryCommand
from app.src.application.category.command.update_category_command_handler import UpdateCategoryCommandHandler
from app.src.application.category.query.get_all_categories_query_handler import GetAllCategoriesQueryHandler
from app.src.application.category.query.is_category_used_query_handler import IsCategoryUsedQueryHandler
from app.src.application.category.service.category_service import CategoryService
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository
from app.src.presentation.form.upsert_category_form import UpsertCategoryForm, UpsertCategoryFormMapper

categories_blueprint = Blueprint('categories_blueprint', __name__, url_prefix='/categories')
category_repository = CategoryRepository()
transaction_repository = TransactionRepository()
category_service = CategoryService(category_repository)


@categories_blueprint.route('/dashboard', methods=['GET'])
def categories_dashboard():
    categories = GetAllCategoriesQueryHandler(category_repository).execute()

    return render_template('categories/categories_dashboard.html',
                           categories=categories,
                           upsert_category_form=UpsertCategoryForm())


@categories_blueprint.route('/create', methods=['POST'])
def create_category():
    form = UpsertCategoryForm(request.form)

    if not form.validate_on_submit():
        flash(gettext("Can't create category. Invalid data"), 'warning')
        return redirect(url_for('categories_blueprint.categories_dashboard'))

    command = UpsertCategoryFormMapper.map_to_create_command(form)
    created: bool = CreateCategoryCommandHandler(category_repository).execute(command)

    if created:
        flash(gettext("Category successfully created!"), "success")
    else:
        flash(gettext("Can't create category"), "warning")

    return redirect(url_for('categories_blueprint.categories_dashboard'))


@categories_blueprint.route('/delete/<int:category_id>', methods=['GET'])
def delete(category_id):
    is_category_used_query_handler = IsCategoryUsedQueryHandler(transaction_repository)
    delete_category_process_manager = DeleteCategoryProcessManager(category_repository, is_category_used_query_handler)

    if delete_category_process_manager.execute(category_id):
        flash(gettext("Category successfully deleted!"), "success")
    else:
        flash(gettext("Can't delete used category!"), "warning")

    return redirect(url_for('categories_blueprint.categories_dashboard'))


@categories_blueprint.route('/edit/<int:category_id>', methods=['POST'])
def edit(category_id):
    form = UpsertCategoryForm(request.form)
    command: UpdateCategoryCommand = UpsertCategoryFormMapper.map_to_update_command(category_id, form)
    UpdateCategoryCommandHandler(category_repository).execute(command)
    return redirect(url_for('categories_blueprint.categories_dashboard'))
