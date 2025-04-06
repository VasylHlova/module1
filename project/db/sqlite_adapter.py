import sqlite3
from typing import Dict, Any, Optional, Union, List, Tuple

class SqliteDatabase:
    """SQLite database adapter implementation.
    
    This class provides methods to interact with SQLite database, handling CRUD
    operations and table creation for the application models.
    
    Attributes:
        db_name (str): Name of the SQLite database file.
        connection: SQLite connection object.
        cursor: SQLite cursor object for executing queries.
    """
    
    def __init__(self, db_name: str = "database.db") -> None:
        """Initialize SQLite database connection.
        
        Args:
            db_name (str, optional): Database file name. Defaults to "database.db".
        """
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        
        # hardcoded tables for demonstration purposes
        self._create_table("user", {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "username": "TEXT",
            "email": "TEXT",
            "created_at": "TEXT"
        })

        self._create_table("product", {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
            "price": "REAL",
            "description": "TEXT",
            "quantity": "INTEGER"
        })
    
    def _create_table(self, table_name: str, schema: Dict[str, str]) -> None:
        """Create a table if it doesn't exist.
        
        Args:
            table_name (str): Name of the table to create.
            schema (Dict[str, str]): Dictionary mapping column names to their SQL types.
        """
        columns = ", ".join([f"{col} {dtype}" for col, dtype in schema.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(query)
        self.connection.commit()    

    def create(self, model_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert a new record into the specified table.
        
        Args:
            model_name (str): Name of the table to insert into.
            data (Dict[str, Any]): Dictionary of column names and values to insert.
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary with the created record including its ID,
                or None if the operation failed.
                
        Raises:
            sqlite3.Error: If there's an issue with the SQL operation.
        """
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            sql = f'INSERT INTO {model_name} ({columns}) VALUES ({placeholders})'
            self.cursor.execute(sql, tuple(data.values()))
            self.connection.commit()
            
            # Get the ID of the inserted row
            last_id = self.cursor.lastrowid
            data['id'] = last_id
            return data
        except sqlite3.Error as e:
            print(f"Error: Your input data is not valid for {model_name} model. {str(e)}")
            return None

    def get(self, model_name: str, obj_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Retrieve a record by ID from the specified table.
        
        Args:
            model_name (str): Name of the table to query.
            obj_id (Union[int, str]): ID of the record to retrieve.
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary with the record data if found,
                or None if not found or an error occurred.
                
        Raises:
            sqlite3.Error: If there's an issue with the SQL operation.
        """
        try:
            sql = f'SELECT * FROM {model_name} WHERE id=?'
            self.cursor.execute(sql, (int(obj_id),))
            row = self.cursor.fetchone()
            
            if row:
                # Convert row to dictionary
                columns = [description[0] for description in self.cursor.description]
                return dict(zip(columns, row))
            return None
        except sqlite3.Error as e:
            print(f"Error retrieving record: {str(e)}")
            return None

    def update(self, model_name: str, obj_id: Union[int, str], 
               data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record by ID in the specified table.
        
        Args:
            model_name (str): Name of the table to update.
            obj_id (Union[int, str]): ID of the record to update.
            data (Dict[str, Any]): Dictionary of column names and values to update.
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary with the updated record if successful,
                or None if not found or an error occurred.
                
        Raises:
            sqlite3.Error: If there's an issue with the SQL operation.
        """
        try:
            set_clause = ', '.join([f'{k}=?' for k in data.keys()])
            sql = f'UPDATE {model_name} SET {set_clause} WHERE id=?'
            self.cursor.execute(sql, (*data.values(), int(obj_id)))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                # Return updated record
                return self.get(model_name, obj_id)
            return None
        except sqlite3.Error as e:
            print(f"Error: Your input data is not valid for {model_name} model. {str(e)}")
            return None

    def delete(self, model_name: str, obj_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Delete a record by ID from the specified table.
        
        Args:
            model_name (str): Name of the table to delete from.
            obj_id (Union[int, str]): ID of the record to delete.
            
        Returns:
            Optional[Dict[str, Any]]: Dictionary with the deleted record data if successful,
                or None if not found or an error occurred.
                
        Raises:
            sqlite3.Error: If there's an issue with the SQL operation.
        """
        try:
            # First get the record to return it after deletion
            record = self.get(model_name, obj_id)
            if not record:
                return None
                
            sql = f'DELETE FROM {model_name} WHERE id=?'
            self.cursor.execute(sql, (int(obj_id),))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return record
            return None
        except sqlite3.Error as e:
            print(f"Error deleting record: {str(e)}")
            return None