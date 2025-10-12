from typing import Type, Dict, Any, Callable
from inspect import signature


# Global registry to map Query classes to Handler classes
_query_handlers: Dict[Type, Type] = {}


def query_handler(query_class: Type):
    """
    Decorator to automatically register query handlers.
    
    Usage:
        @query_handler(GetAllCategoriesQuery)
        class GetAllCategoriesQueryHandler:
            def __init__(self, category_repository):
                ...
    """
    def decorator(handler_class: Type) -> Type:
        _query_handlers[query_class] = handler_class
        return handler_class
    return decorator


def get_handler_for_query(query_class: Type) -> Type:
    """
    Gets the handler class corresponding to a query class.
    
    Args:
        query_class: The query class
        
    Returns:
        The corresponding handler class
        
    Raises:
        ValueError: If no handler is found for the query
    """
    if query_class not in _query_handlers:
        raise ValueError(f"No handler registered for query: {query_class.__name__}")
    
    return _query_handlers[query_class]


def get_available_handlers() -> Dict[str, str]:
    """
    Gets a dictionary with registered handlers for debugging.
    
    Returns:
        Dict with query_name -> handler_name
    """
    return {query_class.__name__: handler_class.__name__ 
            for query_class, handler_class in _query_handlers.items()}


def resolve_handler_dependencies(handler_class: Type, available_repositories: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resolves handler dependencies based on its __init__ parameters.
    
    Args:
        handler_class: The handler class
        available_repositories: Dictionary with available repositories
        
    Returns:
        Dictionary with arguments to instantiate the handler
    """
    try:
        init_signature = signature(handler_class.__init__)
        dependencies = {}
        
        for param_name, param in init_signature.parameters.items():
            if param_name == 'self':
                continue
                
            # Look for repository by parameter name
            if param_name in available_repositories:
                dependencies[param_name] = available_repositories[param_name]
            else:
                # If not found by exact name, search by type
                # This is useful for cases like 'transaction_repo' -> 'transaction_repository'
                for repo_name, repo_instance in available_repositories.items():
                    if param_name.replace('_repo', '_repository') == repo_name:
                        dependencies[param_name] = repo_instance
                        break
                else:
                    raise ValueError(f"Cannot resolve dependency '{param_name}' for handler {handler_class.__name__}")
        
        return dependencies
        
    except Exception as e:
        raise ValueError(f"Error resolving dependencies for {handler_class.__name__}: {str(e)}")
