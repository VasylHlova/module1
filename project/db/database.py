import sys
from typing import Dict, Any, Optional, List, Union
from .sqlite_adapter import SqliteDatabase

sys.path.append('D:\\Code\\labs\\python_labs')

from lab4.minidb.minidb.database import Database


class DatabaseRegistry:
    """Global database registry.
    
    A singleton class that provides a central registry for database instances,
    allowing different parts of the application to access databases by name.
    
    Attributes:
        _databases (dict): Internal storage for database instances.
    """
    _databases: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, db_instance: Any) -> None:
        """Register a database instance with a name.
        
        Args:
            name (str): Unique name for the database instance.
            db_instance (Any): Database instance to register.
        """
        cls._databases[name] = db_instance

    @classmethod
    def get(cls, name: str) -> Optional[Any]:
        """Retrieve a database instance by name.
        
        Args:
            name (str): Name of the database to retrieve.
            
        Returns:
            Optional[Any]: The database instance if found, None otherwise.
        """
        return cls._databases.get(name)

    @classmethod
    def list(cls) -> List[str]:
        """List all registered database names.
        
        Returns:
            List[str]: List of registered database names.
        """
        return list(cls._databases.keys())
    
class CustomDatabase(Database):
    """Custom database implementation extending base Database class.
    
    This class provides in-memory data storage with basic CRUD operations.
    
    Attributes:
        name (str): The name of the database.
        data (dict): In-memory storage for database records.
    """
    def __init__(self, name: str) -> None:
        """Initialize a custom database instance.
        
        Args:
            name (str): The name of the database.
        """
        super().__init__(name)
        self.data: Dict[str, Dict[str, Dict[str, Any]]] = {}
        
    def create(self, model_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a record in the database.
        
        Args:
            model_name (str): The model/collection name.
            data (Dict[str, Any]): Data to store.
            
        Returns:
            Dict[str, Any]: The created record with generated ID.
        """
        if model_name not in self.data:
            self.data[model_name] = {}
        
        # Simple ID generation
        obj_id = str(len(self.data[model_name]) + 1)
        record = dict(data)  # Create a copy of the data
        record['id'] = obj_id
        
        self.data[model_name][obj_id] = record
        return record
    
    def get(self, model_name: str, obj_id: Union[str, int]) -> Optional[Dict[str, Any]]:
        """Get a record by ID.
        
        Args:
            model_name (str): The model/collection name.
            obj_id (Union[str, int]): ID of the record to retrieve.
            
        Returns:
            Optional[Dict[str, Any]]: The record if found, None otherwise.
        """
        obj_id = str(obj_id)
        return self.data.get(model_name, {}).get(obj_id)
    
    def update(self, model_name: str, obj_id: Union[str, int], 
               data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record.
        
        Args:
            model_name (str): The model/collection name.
            obj_id (Union[str, int]): ID of the record to update.
            data (Dict[str, Any]): New data to apply to the record.
            
        Returns:
            Optional[Dict[str, Any]]: The updated record if found and updated,
                None otherwise.
        """
        obj_id = str(obj_id)
        if model_name in self.data and obj_id in self.data[model_name]:
            self.data[model_name][obj_id].update(data)
            return self.data[model_name][obj_id]
        return None
    
    def delete(self, model_name: str, obj_id: Union[str, int]) -> Optional[Dict[str, Any]]:
        """Delete a record.
        
        Args:
            model_name (str): The model/collection name.
            obj_id (Union[str, int]): ID of the record to delete.
            
        Returns:
            Optional[Dict[str, Any]]: The deleted record if found,
                None otherwise.
        """
        obj_id = str(obj_id)
        if model_name in self.data and obj_id in self.data[model_name]:
            deleted = self.data[model_name].pop(obj_id)
            return deleted
        return None   

    def custom_method(self) -> str:
        """Custom method example.
        
        Returns:
            str: A message showing this method was called.
        """
        return f"Custom method called from {self.name}"
    
      
default_db = CustomDatabase("default")
test_db = CustomDatabase("test")
sqlite_db = SqliteDatabase("database.db")

# Register databases
DatabaseRegistry.register("default", default_db)
DatabaseRegistry.register("test", test_db)
DatabaseRegistry.register("sqlite", sqlite_db)

databases = DatabaseRegistry.list()
print(f"Available databases: {databases}")