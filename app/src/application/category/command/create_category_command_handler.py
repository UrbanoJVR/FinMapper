from sqlalchemy import false

from app.src.application.category.command.create_category_command import CreateCategoryCommand
from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class CreateCategoryCommandHandler:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def execute(self, create_category_command: CreateCategoryCommand) -> bool:
        if self.category_repository.exists_by_name(create_category_command.name):
            return False

        self.category_repository.save(
            Category(name=create_category_command.name,
                     description=create_category_command.description))
        return True
