from typing import Dict, Any, Callable

# Dictionary to store all registered routes
ROUTES: Dict[str, Callable] = {}

def route(path: str) -> Callable:
    """Register a function as a route handler.
    
    Args:
        path (str): The route path.
        
    Returns:
        Callable: Decorator function that registers the handler.
    """
    def decorator(func: Callable) -> Callable:
        ROUTES[path] = func
        return func
    return decorator

def handle_request(path: str, **kwargs: Any) -> Any:
    """Handle a request for a given route path.
    
    Args:
        path (str): The request path.
        **kwargs: Request data.
        
    Returns:
        Any: Result of the corresponding handler function,
            or an error message if the route is not found.
    """
    if path in ROUTES:
        return ROUTES[path](**kwargs)
    return {"error": f"Route '{path}' not found"}