from faker import Faker

from app.src.domain.category import Category


class CategoryMother:
    _faker = Faker()

    def random(self):
        return Category(self._faker.word(), self._faker.sentence(), self._faker.random_number())
