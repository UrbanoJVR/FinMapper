from app.src.application.query_bus_registry import get_handler_for_query, resolve_handler_dependencies
from app.src.infrastructure.repository.category_repository import CategoryRepository
from app.src.infrastructure.repository.transaction_repository import TransactionRepository

# Import all handlers so decorators are registered
from app.src.application.category.query.get_all_categories_query_handler import GetAllCategoriesQueryHandler
from app.src.application.dashboard.query.get_latest_available_transaction_year_handler import GetLatestAvailableTransactionYearHandler
from app.src.application.dashboard.query.get_total_expenses_by_year_query_handler import GetTotalExpensesByYearQueryHandler
from app.src.application.transaction.query.get_transaction_by_id_query_handler import GetTransactionByIdQueryHandler
from app.src.application.transaction.query.search_transactions_by_month_year_query_handler import SearchTransactionsByMonthYearQueryHandler
from app.src.application.transaction.query.search_last_uncategorized_transactions_query_handler import SearchLastUncategorizedTransactionsQueryHandler


class QueryBus:

    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.category_repository = CategoryRepository()

    def ask(self, query):
        # Get the corresponding handler using the registry
        handler_class = get_handler_for_query(type(query))
        
        # Prepare available repositories
        available_repositories = {
            'transaction_repository': self.transaction_repository,
            'category_repository': self.category_repository
        }
        
        # Resolve handler dependencies
        dependencies = resolve_handler_dependencies(handler_class, available_repositories)
        
        # Instantiate the handler with resolved dependencies
        handler = handler_class(**dependencies)
        
        # Execute the handler
        # Some handlers need the query as parameter, others don't
        try:
            return handler.execute(query)
        except TypeError:
            # If handler doesn't accept query as parameter, execute without arguments
            return handler.execute()