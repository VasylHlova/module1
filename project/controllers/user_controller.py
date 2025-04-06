from typing import Dict, Any, Optional
from models.user import User
from routes_decorator import route

@route('/sql/users/create')
def sql_create_user(data: Dict[str, Any], model_name: str = "user") -> Dict[str, Any]:
    """Create a new user in SQL database.
    
    Args:
        data (Dict[str, Any]): User data.
        model_name (str, optional): Model name. Defaults to "user".
        
    Returns:
        Dict[str, Any]: Creation result with user data.
    """
    User.use_db("sqlite")
    
    user = User.create(model_name, **data)
    User.use_db("default")
    return {"status": "success", "user": user.to_dict()}

@route('/users/create')
def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new user.
    
    Args:
        data (Dict[str, Any]): User data.
        
    Returns:
        Dict[str, Any]: Creation result with user data.
    """
    user = User.create(**data)
    return {"status": "success", "user": user.to_dict()}

@route('/sql/users/get')
def sql_get_user(user_id: str, model_name: str = "user") -> Dict[str, Any]:
    """Retrieve a user by ID from SQL database.
    
    Args:
        user_id (str): User ID.
        model_name (str, optional): Model name. Defaults to "user".
        
    Returns:
        Dict[str, Any]: User data or error message.
    """
    User.use_db("sqlite")
    user = User.get(model_name, user_id)
    if user:
        User.use_db("default")
        return {"status": "success", "user": user.to_dict()}
        
    User.use_db("default")    
    return {"status": "error", "message": "User not found"}

@route('/users/get')
def get_user(user_id: str) -> Dict[str, Any]:
    """Retrieve a user by ID.
    
    Args:
        user_id (str): User ID.
        
    Returns:
        Dict[str, Any]: User data or error message.
    """
    user = User.get(user_id)
    if user:
        return {"status": "success", "user": user.to_dict()}
    
    return {"status": "error", "message": "User not found"}

@route('/sql/users/update')
def sql_update_user(user_id: str, data: Dict[str, Any], model_name: str = "user") -> Dict[str, Any]:
    """Update user data in SQL database.
    
    Args:
        user_id (str): User ID.
        data (Dict[str, Any]): New user data.
        model_name (str, optional): Model name. Defaults to "user".
        
    Returns:
        Dict[str, Any]: Update result with user data or error message.
    """
    User.use_db("sqlite")
    user = User.update(model_name, user_id, **data)
    if user:
        User.use_db("default")
        return {"status": "success", "user": user.to_dict()}
    User.use_db("default")
    return {"status": "error", "message": "User not found"}

@route('/users/update')
def update_user(user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update user data.
    
    Args:
        user_id (str): User ID.
        data (Dict[str, Any]): New user data.
        
    Returns:
        Dict[str, Any]: Update result with user data or error message.
    """
    user = User.update(user_id, **data)
    if user:
        return {"status": "success", "user": user.to_dict()}
    return {"status": "error", "message": "User not found"}

@route('/sql/users/delete')
def sql_delete_user(user_id: str, model_name: str = "user") -> Dict[str, Any]:
    """Delete a user by ID from SQL database.
    
    Args:
        user_id (str): User ID.
        model_name (str, optional): Model name. Defaults to "user".
        
    Returns:
        Dict[str, Any]: Delete result or error message.
    """
    User.use_db("sqlite")
    result = User.delete(model_name, user_id)
    if result:
        User.use_db("default")
        return {"status": "success", "message": "User deleted"}
    User.use_db("default")
    return {"status": "error", "message": "User not found"}

@route('/users/delete')
def delete_user(user_id: str) -> Dict[str, Any]:
    """Delete a user by ID.
    
    Args:
        user_id (str): User ID.
        
    Returns:
        Dict[str, Any]: Delete result or error message.
    """
    result = User.delete(user_id)
    if result:
        return {"status": "success", "message": "User deleted"}
    return {"status": "error", "message": "User not found"}


