from .base_model import BaseModel

class Product(BaseModel):
    """Product model.
    
    This class represents a product in the system with inventory information
    and product details.
    
    Attributes:
        id (int): Unique identifier for the product.
        name (str): The name of the product.
        description (str): Detailed description of the product.
        price (float): The price of the product in currency units.
        quantity (int): Available inventory quantity.
    """
    id: int
    name: str
    description: str
    price: float
    quantity: int

