from db.database import DatabaseRegistry
from typing import Dict, Any, Optional, Type, ClassVar

class BaseModelMeta(type):
    """Metaclass that registers all models in an internal registry.
    
    This metaclass automatically registers all model classes that inherit from
    BaseModel, making them available through the registry dictionary.
    
    Attributes:
        registry (dict): Dictionary mapping class names to class objects.
    """
    registry: ClassVar[Dict[str, Type]] = {}

    def __new__(cls, name, bases, attrs):
        obj = super().__new__(cls, name, bases, attrs)
        if name != "BaseModel":  # Avoid registering the base class itself
            BaseModelMeta.registry[name] = obj
        return obj

class BaseModel(metaclass=BaseModelMeta):
    """Base model with database selection support.
    
    This class serves as the foundation for all data models in the system,
    providing common database operations and dynamic database selection.
    
    Attributes:
        _db_instance: The database instance used by this model.
    """
    _db_instance = DatabaseRegistry.get("default")  # Default database

    def __init__(self, **kwargs):
        """Initialize a model instance with provided attributes.
        
        Args:
            **kwargs: Key-value pairs representing model attributes.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model instance to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the model.
        """
        
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def use_db(cls, db_name: str) -> None:
        """Dynamically change the database used by this model.
        
        Args:
            db_name (str): Name of the database to use.
            
        Raises:
            ValueError: If the specified database is not found.
        """
        db = DatabaseRegistry.get(db_name)
        if db:
            cls._db_instance = db
        else:
            raise ValueError(f"Database '{db_name}' not found")

    @classmethod
    def create(cls, model_name: Optional[str] = None, **data) -> Optional['BaseModel']:
        """Create a new object in the selected database.
        
        Args:
            model_name (str, optional): Name of the model. If None, uses the class name.
            **data: Attributes for the new object.
            
        Returns:
            BaseModel: New model instance if successful, None otherwise.
        """
        if data:
            model = model_name or cls.__name__.lower()
            record = cls._db_instance.create(model, data)
            
            if record:
                return cls(**record)
        else:
            raise ValueError("No data provided for creation")    
        return None

    @classmethod
    def get(cls, model_name: Optional[str] = None, obj_id: Optional[Any] = None) -> Optional['BaseModel']:
        """Retrieve an object by ID.
        
        Args:
            model_name (str, optional): Name of the model or ID if obj_id is None.
            obj_id (Any, optional): Object ID. If None, model_name is used as ID.
            
        Returns:
            BaseModel: Model instance if found, None otherwise.
        """
        if obj_id is None:
            obj_id = model_name
            model_name = cls.__name__.lower()
        record = cls._db_instance.get(model_name, obj_id)
    
        if record:
            return cls(**record)
        return None
        
    @classmethod
    def update(cls, model_name: Optional[str] = None, obj_id: Optional[Any] = None, **data) -> Optional['BaseModel']:
        """Update an object by ID.
        
        Args:
            model_name (str, optional): Name of the model or ID if obj_id is None.
            obj_id (Any, optional): Object ID. If None, model_name is used as ID.
            **data: Attributes to update.
            
        Returns:
            BaseModel: Updated model instance if successful, None otherwise.
        """
        if data:
            if obj_id is None:
                obj_id = model_name
                model_name = cls.__name__.lower()
            record = cls._db_instance.update(model_name, obj_id, data)
            
            if record:
                return cls(**record)
        else:
            raise ValueError("No data provided for update")    
        return None

    @classmethod
    def delete(cls, model_name: Optional[str] = None, obj_id: Optional[Any] = None) -> Optional['BaseModel']:
        """Delete an object by ID.
        
        Args:
            model_name (str, optional): Name of the model or ID if obj_id is None.
            obj_id (Any, optional): Object ID. If None, model_name is used as ID.
            
        Returns:
            BaseModel: Deleted model instance if successful, None otherwise.
        """
        if obj_id is None:
            obj_id = model_name
            model_name = cls.__name__.lower()
        record = cls._db_instance.delete(model_name, obj_id)
        
        if record:
            return cls(**record)
        return None
