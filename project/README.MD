
## Features

* Multiple database support (SQLite and custom in-memory implementation)
* Dynamic database switching for models

* Centralized database registry
* Decorator-based routing system

* Complete CRUD operations for models
* Type hinting for better IDE support

* Metaclass-based model registry





## Project Structure

```
project/
├── db/
│   ├── database.py         # Database registry and custom implementation
│   └── sqlite_adapter.py   # SQLite database adapter
├── models/
│   ├── base_model.py       # Base model with common functionality
│   ├── product.py          # Product model definition
│   └── user.py             # User model definition (not shown in attachments)
├── controllers/
│   ├── database_controller.py  # Database management endpoints
│   ├── product_controller.py   # Product CRUD endpoints
│   └── user_controller.py      # User CRUD endpoints
├── tests/
│   ├── test_crud_api.py  
└── routes_decorator.py     # Route registration system
└── main.py   
└── requirements.txt   
```



## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/database-abstraction-framework.git
cd database-abstraction-framework
```


2. Install required dependencies:

```bash
pip install reuirements.tx
```

3. Import the project modules in your application


## Usage

### Basic Model Operations

```python
from models.user import User
from models.product import Product
#Create a new 
useruser = User.create(username="johndoe", email="john@example.com")
#Retrieve a user by ID
user = User.get("1")
#Update a 
userupdated_user = User.update("1", username="johnupdated")Delete a userUser.delete("1")
```


### Switching Databases

```python
#Switch to SQLite database for User model
User.use_db("sqlite")
#Switch back to default in-memory 
databaseUser.use_db("default")
```



### Using the Route System

```python
from routes_decorator import handle_request

#Create a new product
result = handle_request('/products/create', data={
    "name": "Laptop",
    "price": 999.99,
    "description": "Powerful laptop",
    "quantity": 10
})

#Get a product
result = handle_request('/products/get', product_id="1")

#Create a user in SQLite database
result = handle_request('/sql/users/create', data={
    "username": "alice",
    "email": "alice@example.com"
})
```


## Database System

The project includes two database implementations:

1. **CustomDatabase** : An in-memory database for quick testing and development
2. **SqliteDatabase** : A persistent SQLite-based database

The [DatabaseRegistry](vscode-file://vscode-app/d:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) provides a central point for registering and accessing database instances:

```python
#List all available databases
from db.database import DatabaseRegistry
databases = DatabaseRegistry.list()
```


## Models

Models inherit from [BaseModel](vscode-file://vscode-app/d:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html) which provides common CRUD operations:

* [create()](vscode-file://vscode-app/d:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Create a new record
* [get()](vscode-file://vscode-app/d:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Retrieve a record by ID
* [update()](vscode-file://vscode-app/d:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Update a record
* [delete()](vscode-file://vscode-app/d:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html): Delete a record

Models are automatically registered through a metaclass system.


## Routes and Controllers

The routing system provides HTTP-like endpoints for accessing model functionality:

* `/users/create`, `/users/get`, etc. - In-memory database operations
* `/sql/users/create`, `/sql/users/get`, etc. - SQLite database operations
* `/database/switch`, `/database/list`, etc. - Database management

Routes are defined using the `@route` decorator:

```python
from routes_decorator import route
@route('/example/path')
def example_handler(param1, param2):
    # Handler implementation
    return {"status": "success", "data": result}
```


## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: [git commit -m &#39;Add feature&#39;](vscode-file://vscode-app/d:/Users/User/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request
