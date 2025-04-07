from typing import Dict, Any
from models.product import Product
from routes_decorator import route

@route('/sql/products/create')
def sql_create_product(data: Dict[str, Any], model_name: str = "product") -> Dict[str, Any]:
    """Create a new product in SQL database.
    
    Args:
        data (Dict[str, Any]): Product data.
        model_name (str, optional): Model name. Defaults to "product".
        
    Returns:
        Dict[str, Any]: Creation result with product data.
    """
    Product.use_db("sqlite")
    
    product = Product.create(model_name, **data)
    if not product:
        Product.use_db("default")
        return {"status": "error", "message": "Product creation failed"}
    Product.use_db("default")
    return {"status": "success", "product": product.to_dict()}

@route('/products/create')
def create_product(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new product.
    
    Args:
        data (Dict[str, Any]): Product data.
        
    Returns:
        Dict[str, Any]: Creation result with product data.
    """
    product = Product.create(**data)
    if not product:
        return {"status": "error", "message": "Product creation failed"}
    return {"status": "success", "product": product.to_dict()}

@route('/sql/products/get')
def sql_get_product(product_id: str, model_name: str = "product") -> Dict[str, Any]:
    """Retrieve a product by ID from SQL database.
    
    Args:
        product_id (str): Product ID.
        model_name (str, optional): Model name. Defaults to "product".
        
    Returns:
        Dict[str, Any]: Product data or error message.
    """
    Product.use_db("sqlite")
    product = Product.get(model_name, product_id)
    if product:
        Product.use_db("default")
        return {"status": "success", "product": product.to_dict()}
        
    Product.use_db("default")    
    return {"status": "error", "message": "Product not found"}

@route('/products/get')
def get_product(product_id: str) -> Dict[str, Any]:
    """Retrieve a product by ID.
    
    Args:
        product_id (str): Product ID.
        
    Returns:
        Dict[str, Any]: Product data or error message.
    """
    product = Product.get(product_id)
    if product:
        return {"status": "success", "product": product.to_dict()}
    
    return {"status": "error", "message": "Product not found"}

@route('/sql/products/update')
def sql_update_product(product_id: str, data: Dict[str, Any], model_name: str = "product") -> Dict[str, Any]:
    """Update product data in SQL database.
    
    Args:
        product_id (str): Product ID.
        data (Dict[str, Any]): New product data.
        model_name (str, optional): Model name. Defaults to "product".
        
    Returns:
        Dict[str, Any]: Update result with product data or error message.
    """
    Product.use_db("sqlite")
    product = Product.update(model_name, product_id, **data)
    if product:
        Product.use_db("default")
        return {"status": "success", "product": product.to_dict()}
    Product.use_db("default")
    return {"status": "error", "message": "Product not found"}

@route('/products/update')
def update_product(product_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update product data.
    
    Args:
        product_id (str): Product ID.
        data (Dict[str, Any]): New product data.
        
    Returns:
        Dict[str, Any]: Update result with product data or error message.
    """
    product = Product.update(product_id, **data)
    if product:
        return {"status": "success", "product": product.to_dict()}
    return {"status": "error", "message": "Product not found"}

@route('/sql/products/delete')
def sql_delete_product(product_id: str, model_name: str = "product") -> Dict[str, Any]:
    """Delete a product by ID from SQL database.
    
    Args:
        product_id (str): Product ID.
        model_name (str, optional): Model name. Defaults to "product".
        
    Returns:
        Dict[str, Any]: Delete result or error message.
    """
    Product.use_db("sqlite")
    result = Product.delete(model_name, product_id)
    if result:
        Product.use_db("default")
        return {"status": "success", "message": "Product deleted"}
    Product.use_db("default")
    return {"status": "error", "message": "Product not found"}

@route('/products/delete')
def delete_product(product_id: str) -> Dict[str, Any]:
    """Delete a product by ID.
    
    Args:
        product_id (str): Product ID.
        
    Returns:
        Dict[str, Any]: Delete result or error message.
    """
    result = Product.delete(product_id)
    if result:
        return {"status": "success", "message": "Product deleted"}
    return {"status": "error", "message": "Product not found"}