from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository



class TestCategoryRepositoryIT:

    def setup_method(self):
        self.sut = CategoryRepository()

    def test_autoincrement_id_on_create(self, db_test):
        category = Category(name="test name", description="test description")

        self.sut.save(category)

        category = self.sut.get_by_name(category.name)
        assert category.id == 1
