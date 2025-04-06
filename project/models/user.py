from .base_model import BaseModel

class User(BaseModel):
    """User model.
    
    This class represents a user in the system and stores basic
    user information and account details.
    
    Attributes:
        id (int): Unique identifier for the user.
        username (str): The user's display name in the system.
        email (str): The user's email address for notifications and login.
        created_at (str): Timestamp when the user account was created.
    """
    id: int
    username: str
    email: str
    created_at: str


