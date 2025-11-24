from app.src.application.category.query.is_category_used_query_handler import IsCategoryUsedQueryHandler
from app.src.infrastructure.repository.category_repository import CategoryRepository


class DeleteCategoryProcessManager:

    def __init__(self, category_repository: CategoryRepository,
                 is_category_used_query_handler: IsCategoryUsedQueryHandler):
        self.category_repository = category_repository
        self.is_category_used_query_handler = is_category_used_query_handler

    def execute(self, category_id: int) -> bool:
        if self.is_category_used_query_handler.execute(category_id):
            return False

        self.category_repository.delete_by_id(category_id)
        return True
