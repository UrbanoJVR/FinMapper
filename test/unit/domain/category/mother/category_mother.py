from faker import Faker

from app.src.domain.category import Category


class CategoryMother:
    _faker = Faker()

    def random(self):
        return Category(self._faker.word(), self._faker.sentence(), self._faker.random_number())

    def random_with_id(self, category_id: int) -> Category:
        return Category(self._faker.word(), self._faker.sentence(), category_id)

    def random_with_name(self, name: str) -> Category:
        return Category(name, self._faker.sentence(), self._faker.random_number())

    def random_with_name_and_id(self, name: str, category_id: int) -> Category:
        return Category(name, self._faker.sentence(), category_id)
