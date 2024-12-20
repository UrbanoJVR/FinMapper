from app.src.application.category.command.update_category_command import UpdateCategoryCommand
from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class UpdateCategoryCommandHandler:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, command: UpdateCategoryCommand):
        category = self.category_repository.get_by_id(command.category_id)

        if category is None:
            return

        category = self._update_category_from_command(command)
        self.category_repository.update(category)

    @staticmethod
    def _update_category_from_command(command: UpdateCategoryCommand) -> Category:
        return Category(id=command.category_id, name=command.category_name, description=command.category_description)
