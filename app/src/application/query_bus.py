from app.src.application.category.query.get_all_categories_query_handler import GetAllCategoriesQuery, \
    GetAllCategoriesQueryHandler
from app.src.application.transaction.query.get_transaction_by_id_query_handler import GetTransactionByIdQuery, \
    GetTransactionByIdQueryHandler
from app.src.application.transaction.query.search_transactions_by_month_year_query import \
    SearchTransactionsByMonthYearQuery
from app.src.application.transaction.query.search_transactions_by_month_year_query_handler import \
    SearchTransactionsByMonthYearQueryHandler
from app.src.application.transaction.query.search_last_uncategorized_transactions_query_handler import \
    SearchLastUncategorizedTransactionsQueryHandler, SearchLastUncategorizedTransactionsQuery
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository


class QueryBus:

    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.category_repository = CategoryRepository()

    def ask(self, query):
        if isinstance(query, SearchTransactionsByMonthYearQuery):
            handler = SearchTransactionsByMonthYearQueryHandler(self.transaction_repository)
            return handler.execute(query)

        if isinstance(query, SearchLastUncategorizedTransactionsQuery):
            handler = SearchLastUncategorizedTransactionsQueryHandler(self.transaction_repository)
            return handler.execute()

        if isinstance(query, GetAllCategoriesQuery):
            handler = GetAllCategoriesQueryHandler(self.category_repository)
            return handler.execute()

        if isinstance(query, GetTransactionByIdQuery):
            handler = GetTransactionByIdQueryHandler(self.transaction_repository)
            return handler.execute(query)