from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from security.jwt import verify_access_token

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Extract and validate the current user from JWT.
    """
    token = credentials.credentials
    try:
        user_data = verify_access_token(token)
        return user_data  # Returns user info (e.g., {"sub": "admin", "role": "admin"})
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
