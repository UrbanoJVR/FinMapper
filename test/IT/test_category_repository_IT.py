from app.src.domain.category import Category
from app.src.infrastructure.repository.category_repository import CategoryRepository


class TestCategoryRepositoryIT:

    def setup_method(self):
        self.sut = CategoryRepository()

    def test_autoincrement_id_on_create(self, db_test_it):
        category = Category(name="test name", description="test description")

        self.sut.save(category)

        category = self.sut.get_by_name(category.name)
        assert category.id == 1

    def test_save_and_find_all(self, db_test_it):
        category1 = Category(name="test name", description="test description")
        category2 = Category(name="test name 2", description="test description 2")

        self.sut.save(category1)
        self.sut.save(category2)
        categories = self.sut.get_all()

        assert len(categories) == 2
        assert categories[0].id == 1
        assert categories[1].id == 2
        assert categories[0].name == category1.name
        assert categories[1].name == category2.name

    def test_delete(self, db_test_it):
        category1 = Category(name="test name", description="test description")
        category2 = Category(name="test name 2", description="test description 2")
        self.sut.save(category1)
        self.sut.save(category2)

        category_to_delete = self.sut.get_by_name(category1.name)
        self.sut.delete_by_id(category_to_delete.id)

        categories = self.sut.get_all()
        assert len(categories) == 1
        assert categories[0].name == category2.name

    def test_update(self, db_test_it):
        category = Category(name="test name", description="test description")
        self.sut.save(category)
        category = self.sut.get_by_name(category.name)
        category_to_update = Category(id=category.id, name="new name", description="new description")

        self.sut.update(category_to_update)
        updated_category = self.sut.get_by_name(category_to_update.name)
        assert updated_category.name == category_to_update.name
        assert updated_category.description == category_to_update.description

    def test_get_by_id(self, db_test_it):
        category = Category(id=1, name="test name", description="test description")
        self.sut.save(category)

        result = self.sut.get_by_id(category.id)
        assert result == category

    def test_get_by_id_return_none(self, db_test_it):
        result = self.sut.get_by_id(1)

        assert result is None

    def test_exists_by_name_return_true(self, db_test_it):
        category = Category(name="test name", description="test description")
        self.sut.save(category)

        result = self.sut.exists_by_name(category.name)

        assert result is True

    def test_exists_by_name_return_false(self, db_test_it):
        result = self.sut.exists_by_name("Name that doesn't exist")

        assert result is False

    def test_get_by_name(self, db_test_it):
        category = Category(id=1, name="test name", description="test description")
        self.sut.save(category)

        result = self.sut.get_by_name(category.name)

        assert result == category

    def test_get_by_name_when_no_exists(self, db_test_it):
        result = self.sut.get_by_name("Name that doesn't exist")

        assert result is None