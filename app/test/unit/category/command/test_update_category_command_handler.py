from unittest import TestCase
from unittest.mock import Mock

from app.src.application.category.command.update_category_command import UpdateCategoryCommand
from app.src.application.category.command.update_category_command_handler import UpdateCategoryCommandHandler
from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TestUpdateCategoryCommandHandler(TestCase):

    def setUp(self):
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.sut = UpdateCategoryCommandHandler(self.mock_category_repository)

    def test_execute_do_nothing(self):
        self.mock_category_repository.get_by_id.return_value = None
        command = UpdateCategoryCommand(category_id=1, category_name="test", category_description="test")

        self.sut.execute(command)

        self.mock_category_repository.update.assert_not_called()

    def test_execute_should_update_category(self):
        category_from_db = Category(id=1, name="test", description="description")
        command = UpdateCategoryCommand(category_id=1, category_name="new name", category_description="new description")
        updated_category = Category(id=command.category_id, name=command.category_name,
                                    description=command.category_description)
        self.mock_category_repository.get_by_id.return_value = category_from_db

        self.sut.execute(command)
        self.mock_category_repository.update.assert_called_once_with(updated_category)
