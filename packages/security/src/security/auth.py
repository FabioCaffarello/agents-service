from security.jwt import create_access_token
from datetime import timedelta

# Simulating a fake in-memory user store
FAKE_USERS_DB = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user1": {"username": "user1", "password": "password123", "role": "agent"},
}


def authenticate_user(username: str, password: str):
    """
    Validate user credentials.
    """
    user = FAKE_USERS_DB.get(username)
    if not user or user["password"] != password:
        return None  # Invalid credentials
    return user


def login_user(username: str, password: str):
    """
    Authenticate and return a JWT token if successful.
    """
    user = authenticate_user(username, password)
    if not user:
        return None  # Invalid login

    access_token = create_access_token(
        {"sub": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=30),
    )
    return access_token
