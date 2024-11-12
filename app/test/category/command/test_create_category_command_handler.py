from unittest.mock import Mock

from app.src.application.category.command.create_category_command import CreateCategoryCommand
from app.src.application.category.command.create_category_command_handler import CreateCategoryCommandHandler
from app.src.presentation.routes.category_routes import category_repository

mock_repository = Mock(spec=category_repository)
sut = CreateCategoryCommandHandler(category_repository=mock_repository)


def test_execute_success():
    command = CreateCategoryCommand(name='Name', description='Description')
    mock_repository.exists_by_name.return_value = False

    result = sut.execute(command)

    assert result is True
    mock_repository.exists_by_name.assert_called_once_with(command.name)
    mock_repository.save.assert_called_once()

def test_execute_when_category_name_exists():
    command = CreateCategoryCommand(name='Name', description='Description')
    mock_repository.exists_by_name.return_value = True

    result = sut.execute(command)

    assert result is False
    mock_repository.exists_by_name.assert_called_once_with(command.name)
    mock_repository.save.assert_not_called()
