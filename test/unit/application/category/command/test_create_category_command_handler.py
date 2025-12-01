import unittest
from unittest.mock import Mock

from app.src.application.category.command.create_category_command import CreateCategoryCommand
from app.src.application.category.command.create_category_command_handler import CreateCategoryCommandHandler
from app.src.infrastructure.repository.category_repository import CategoryRepository

class TestCreateCategoryCommandHandler(unittest.TestCase):

    def setUp(self):
        self.mock_repository = Mock(spec=CategoryRepository)
        self.sut = CreateCategoryCommandHandler(category_repository=self.mock_repository)

    def test_execute_success(self):
        command = CreateCategoryCommand(name='Name', description='Description')
        self.mock_repository.exists_by_name.return_value = False

        result = self.sut.execute(command)

        assert result is True
        self.mock_repository.exists_by_name.assert_called_once_with(command.name)
        self.mock_repository.save.assert_called_once()

    def test_not_create_when_category_name_exists(self):
        command = CreateCategoryCommand(name='Name', description='Description')
        self.mock_repository.exists_by_name.return_value = True

        result = self.sut.execute(command)

        assert result is False
        self.mock_repository.exists_by_name.assert_called_once_with(command.name)
        self.mock_repository.save.assert_not_called()
