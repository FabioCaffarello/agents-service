from fastapi import HTTPException, Security, WebSocket
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


async def get_current_user_ws(websocket: WebSocket):
    # Manually extract the Authorization header from the WebSocket handshake.
    token_header = websocket.headers.get("Authorization")
    if not token_header:
        await websocket.close(code=1008)
        raise Exception("Missing authorization header")
    try:
        # Expect header format: "Bearer <token>"
        scheme, token = token_header.split()
        if scheme.lower() != "bearer":
            await websocket.close(code=1008)
            raise Exception("Invalid authentication scheme")
    except Exception as e:
        await websocket.close(code=1008)
        raise e

    try:
        # Verify the token
        user = verify_access_token(token)
        return user
    except Exception as e:
        await websocket.close(code=1008)
        raise e
