from controllers.user_controller import *
from controllers.database_controller import *
from routes_decorator import handle_request
from datetime import datetime



print("=== Default Database ===")
print(handle_request("/users/create", data={"name": "Alice", "email": "alice@example.com", 'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}))
print(handle_request("/users/create", data={"name": "Bob", "email": "bob@example.com", 'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}))
print(handle_request("/users/get", user_id=1))


print("\n=== Switching to test database ===")
print(handle_request("/database/switch", model_name="User", db_name="test"))
    
print("\n=== Creating user in test database ===")
print(handle_request("/users/create", data={"name": "Charlie", "email": "charlie@example.com", 'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}))
    
print("\n=== Getting users from different databases ===")
print(handle_request("/database/switch", model_name="User", db_name="default"))
print("Default DB:", handle_request("/users/get", user_id=1))  
print(handle_request("/database/switch", model_name="User", db_name="test"))
print("Test DB:", handle_request("/users/get", user_id=1)) 

print("\n=== Updating user ===")
print(handle_request("/users/update", user_id=1, data={"name": "Alice Updated"}))

print("\n=== Deleting user ===")
print(handle_request("/users/delete", user_id=2))

print("\n=== Using to sqlite database ===")
print(handle_request("/database/switch", model_name="User", db_name="sqlite"))


print("\n=== Getting user from sqlite ===")
print(handle_request("/sql/users/get", user_id=4))  



