import pytest
from unittest.mock import patch, MagicMock
import sys


# Add project root to path to make imports work
sys.path.append('D:\\Code\\labs\\python_labs\\module.py\\project')

from controllers.user_controller import *
from controllers.product_controller import *
from controllers.database_controller import *
from models.user import User
from models.product import Product
from routes_decorator import route, handle_request, ROUTES


# --- User Controller Tests ---

@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    user = MagicMock()
    user.to_dict.return_value = {"id": "1", "username": "test_user", "email": "test@example.com"}
    return user


def test_create_user_valid_data(mock_user):
    """Test creating a user with valid data."""
    with patch.object(User, 'create', return_value=mock_user):
        result = create_user({"username": "test_user", "email": "test@example.com"})
        assert result["status"] == "success"
        assert result["user"] == mock_user.to_dict()


def test_create_user_empty_data():
    """Test creating a user with empty data."""
    with patch.object(User, 'create', return_value=None):
        result = create_user({})
        assert "user" not in result


def test_get_user_existing(mock_user):
    """Test retrieving an existing user."""
    with patch.object(User, 'get', return_value=mock_user):
        result = get_user("1")
        assert result["status"] == "success"
        assert result["user"] == mock_user.to_dict()


def test_get_user_nonexistent():
    """Test retrieving a non-existent user."""
    with patch.object(User, 'get', return_value=None):
        result = get_user("999")
        assert result["status"] == "error"
        assert "not found" in result["message"]


def test_update_user_valid_data(mock_user):
    """Test updating a user with valid data."""
    with patch.object(User, 'update', return_value=mock_user):
        result = update_user("1", {"username": "updated_user"})
        assert result["status"] == "success"
        assert result["user"] == mock_user.to_dict()


def test_update_user_nonexistent():
    """Test updating a non-existent user."""
    with patch.object(User, 'update', return_value=None):
        result = update_user("999", {"username": "updated_user"})
        assert result["status"] == "error"
        assert "not found" in result["message"]


def test_delete_user_existing():
    """Test deleting an existing user."""
    with patch.object(User, 'delete', return_value={"id": "1"}):
        result = delete_user("1")
        assert result["status"] == "success"
        assert "deleted" in result["message"]


def test_delete_user_nonexistent():
    """Test deleting a non-existent user."""
    with patch.object(User, 'delete', return_value=None):
        result = delete_user("999")
        assert result["status"] == "error"
        assert "not found" in result["message"]


# --- SQL User Controller Tests ---

def test_sql_create_user_valid_data(mock_user):
    """Test creating a user in SQL with valid data."""
    with patch.object(User, 'create', return_value=mock_user), \
         patch.object(User, 'use_db'):
        result = sql_create_user({"username": "test_user", "email": "test@example.com"})
        assert result["status"] == "success"
        assert result["user"] == mock_user.to_dict()
        User.use_db.assert_any_call("sqlite")
        User.use_db.assert_any_call("default")


def test_sql_get_user_with_invalid_id():
    """Test retrieving a user from SQL with invalid ID."""
    with patch.object(User, 'get', return_value=None), \
         patch.object(User, 'use_db'):
        result = sql_get_user("invalid_id")
        assert result["status"] == "error"
        assert "not found" in result["message"]


# --- Product Controller Tests ---

@pytest.fixture
def mock_product():
    """Create a mock product for testing."""
    product = MagicMock()
    product.to_dict.return_value = {"id": "1", "name": "Test Product", "price": 99.99, "quantity": 10}
    return product


def test_create_product_valid_data(mock_product):
    """Test creating a product with valid data."""
    with patch.object(Product, 'create', return_value=mock_product):
        result = create_product({"name": "Test Product", "price": 99.99, "quantity": 10})
        assert result["status"] == "success"
        assert result["product"] == mock_product.to_dict()


def test_create_product_invalid_data():
    """Test creating a product with invalid data."""
    with patch.object(Product, 'create', side_effect=ValueError("Invalid price")):
        try:
            result = create_product({"name": "Test Product", "price": "invalid_price"})
            assert False, "Should have raised an exception"
        except ValueError:
            assert True


def test_get_product_existing(mock_product):
    """Test retrieving an existing product."""
    with patch.object(Product, 'get', return_value=mock_product):
        result = get_product("1")
        assert result["status"] == "success"
        assert result["product"] == mock_product.to_dict()


def test_update_product_valid_data(mock_product):
    """Test updating a product with valid data."""
    with patch.object(Product, 'update', return_value=mock_product):
        result = update_product("1", {"price": 149.99})
        assert result["status"] == "success"
        assert result["product"] == mock_product.to_dict()


def test_sql_delete_product_existing():
    """Test deleting an existing product from SQL."""
    with patch.object(Product, 'delete', return_value={"id": "1"}), \
         patch.object(Product, 'use_db'):
        result = sql_delete_product("1")
        assert result["status"] == "success"
        assert "deleted" in result["message"]


# --- Database Controller Tests ---

def test_switch_database_valid_model():
    """Test switching database for a valid model."""
    with patch.object(User, 'use_db'):
        result = switch_database("User", "sqlite")
        assert "error" not in result
        assert "Switched User" in result["message"]


def test_switch_database_invalid_model():
    """Test switching database for an invalid model."""
    result = switch_database("InvalidModel", "sqlite")
    assert "error" in result
    assert "Model not found" in result["error"]


def test_switch_database_invalid_db():
    """Test switching to an invalid database."""
    with patch.object(User, 'use_db', side_effect=ValueError("Database not found")):
        result = switch_database("User", "invalid_db")
        assert "error" in result
        assert "Database not found" in result["error"]


def test_list_databases():
    """Test listing available databases."""
    with patch('db.database.DatabaseRegistry.list', return_value=["default", "sqlite", "test"]):
        result = list_databases()
        assert "databases" in result
        assert "default" in result["databases"]
        assert "sqlite" in result["databases"]


def test_get_database_info_existing():
    """Test getting info about an existing database."""
    mock_db = MagicMock()
    mock_db.__class__.__name__ = "SqliteDatabase"
    
    with patch('db.database.DatabaseRegistry.get', return_value=mock_db):
        result = get_database_info("sqlite")
        assert "info" in result
        assert result["info"]["name"] == "sqlite"
        assert result["info"]["type"] == "SqliteDatabase"


def test_get_database_info_nonexistent():
    """Test getting info about a non-existent database."""
    with patch('db.database.DatabaseRegistry.get', return_value=None):
        result = get_database_info("nonexistent")
        assert "error" in result
        assert "not found" in result["error"]


def test_get_available_models():
    """Test getting available models."""
    with patch('models.base_model.BaseModelMeta.registry', {"User": User, "Product": Product}):
        result = get_available_models()
        assert "models" in result
        assert "User" in result["models"]
        assert "Product" in result["models"]


# --- Route Handling Tests ---

def test_handle_request_existing_route():
    """Test handling an existing route."""
    test_path = "/test/route"
    test_handler = MagicMock(return_value={"status": "success"})
    
    # Register a test route
    ROUTES[test_path] = test_handler
    
    result = handle_request(test_path, param="value")
    assert result["status"] == "success"
    test_handler.assert_called_once_with(param="value")
    
    # Clean up
    del ROUTES[test_path]


def test_handle_request_nonexistent_route():
    """Test handling a non-existent route."""
    result = handle_request("/nonexistent/route")
    assert "error" in result
    assert "not found" in result["error"]


def test_route_decorator():
    """Test the route decorator."""
    test_path = "/decorator/test"
    
    @route(test_path)
    def test_function(param=None):
        return {"param": param}
    
    assert test_path in ROUTES
    assert ROUTES[test_path] == test_function
    
    result = handle_request(test_path, param="test_value")
    assert result["param"] == "test_value"
    
    # Clean up
    del ROUTES[test_path]


# --- Edge Cases and Invalid Input Tests ---

def test_create_user_special_characters():
    """Test creating a user with special characters in the data."""
    user_data = {"username": "user!@#$%^&*()", "email": "special@example.com"}
    with patch.object(User, 'create', return_value=MagicMock()) as mock_create:
        create_user(user_data)
        mock_create.assert_called_once_with(**user_data)


def test_get_user_non_numeric_id():
    """Test retrieving a user with a non-numeric ID."""
    with patch.object(User, 'get', return_value=None):
        result = get_user("abc123")
        assert result["status"] == "error"
        assert "not found" in result["message"]


def run_tests_and_display_results():
    """Run all tests and display the results."""
    import pytest
    
    print("\n=== RUNNING TESTS ===")
    # Run tests with verbose flag to show detailed output
    exit_code = pytest.main(["-v", __file__])
    print(f"\nTest run completed with exit code: {exit_code}")
    print("=== END OF TEST RUN ===\n")
    
    return exit_code


if __name__ == "__main__":
    try:
        run_tests_and_display_results()
    except Exception as e:
        print(f"Error running tests: {e}")