from unittest import TestCase
from unittest.mock import Mock

from app.src.application.category.query.GetAllCategoriesQueryHandler import GetAllCategoriesQueryHandler
from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TestGetAllCategoriesQueryHandler(TestCase):

    def setUp(self):
        self.mock_category_repository = Mock(spec=CategoryRepository)
        self.sut = GetAllCategoriesQueryHandler(self.mock_category_repository)

    def test_execute(self):
        expected_categories = [Category(id=1, description="Description", name="Category1")]
        self.mock_category_repository.get_all.return_value = expected_categories

        result = self.sut.execute()

        assert result == expected_categories
