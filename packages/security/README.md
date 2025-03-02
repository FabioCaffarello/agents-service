# Security

This package provides a simple JWT-based authentication system using FastAPI and PyJWT. It includes functions for creating and verifying access tokens, authenticating users against an in-memory database, and retrieving the current user from a JWT.

## Features

- **User Authentication:** Validate user credentials against a simulated in-memory database.
- **JWT Token Generation:** Create JWT access tokens with configurable expiration.
- **Token Verification:** Decode and verify JWT tokens to ensure secure access.
- **FastAPI Integration:** Includes a FastAPI security dependency to extract and verify tokens in protected routes.

## Usage

### Simulated User Database

The package includes a simulated user store (`FAKE_USERS_DB`) with sample users:

```python
FAKE_USERS_DB = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user1": {"username": "user1", "password": "password123", "role": "agent"},
}
```

### Authentication and Token Creation

- **Authenticate a user:** Use the `authenticate_user` function to verify user credentials.
- **Login and get token:** The `login_user` function authenticates a user and returns a JWT token.

Example:

```python
from datetime import timedelta
from security.jwt import create_access_token

# Attempt to login as admin
token = login_user("admin", "admin123")
if token:
    print("JWT Token:", token)
else:
    print("Invalid credentials")
```

### Token Verification and FastAPI Integration

- **Token verification:** The `verify_access_token` function decodes and validates the token.
- **FastAPI Security Dependency:** Use `get_current_user` in your FastAPI routes to extract user information.

Example FastAPI route:

```python
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()
security = HTTPBearer()

@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Security(security)):
    user = get_current_user(credentials)
    return {"message": f"Hello, {user['sub']}! Your role is {user['role']}"}
```

### JWT Configuration

- **Secret Key:** The JWT secret key is loaded from the environment variable `JWT_SECRET_KEY`. If not provided, it defaults to `"supersecretkey"`. **Make sure to change this in production.**
- **Algorithm:** Uses `HS256` for token encoding and decoding.
- **Expiration:** Tokens expire in 30 minutes by default. This can be adjusted via the `ACCESS_TOKEN_EXPIRE_MINUTES` variable.

## Environment Variables

- **JWT_SECRET_KEY:** The secret key used to sign JWT tokens. (Default: `supersecretkey`)

Example (on Unix-like systems):

```bash
export JWT_SECRET_KEY="your-production-secret-key"
```
