from typing import Dict, Any
from models.user import User
from models.product import Product
from routes_decorator import route

@route('/database/switch')
def switch_database(model_name: str, db_name: str) -> Dict[str, Any]:
    """Switch a model to use a different database.
    
    Args:
        model_name (str): Name of the model (e.g., "User" or "Product").
        db_name (str): Name of the database to switch to.
        
    Returns:
        Dict[str, Any]: Success message or error information.
    """
    model_mapping = {
        "User": User,
        "Product": Product,
    }
    model = model_mapping.get(model_name)
    if model:
        try:
            model.use_db(db_name)
            return {"message": f"Switched {model_name} to {db_name} database."}
        except Exception as e:
            return {"error": str(e)}
    return {"error": "Model not found"}

@route('/database/list')
def list_databases() -> Dict[str, Any]:
    """Get a list of all available databases.
    
    Returns:
        Dict[str, Any]: Dictionary containing the list of available databases.
    """
    from db.database import DatabaseRegistry
    databases = DatabaseRegistry.list()
    return {"databases": databases}

@route('/database/info')
def get_database_info(db_name: str) -> Dict[str, Any]:
    """Get information about a specific database.
    
    Args:
        db_name (str): Name of the database.
        
    Returns:
        Dict[str, Any]: Database information or error message.
    """
    from db.database import DatabaseRegistry
    db = DatabaseRegistry.get(db_name)
    if db:
        info = {
            "name": db_name,
            "type": db.__class__.__name__,
        }
        return {"info": info}
    return {"error": f"Database '{db_name}' not found"}

@route('/database/models')
def get_available_models() -> Dict[str, Any]:
    """Get a list of all available models.
    
    Returns:
        Dict[str, Any]: Dictionary containing the list of available models.
    """
    from models.base_model import BaseModelMeta
    models = list(BaseModelMeta.registry.keys())
    return {"models": models}