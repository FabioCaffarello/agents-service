from fastapi import APIRouter, HTTPException
from security.auth import login_user
from application.dtos.auth_dto import LoginDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=dict, status_code=200)
def login(request: LoginDTO):
    """
    Authenticate user and return a JWT token.
    """
    token = login_user(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"access_token": token, "token_type": "bearer"}
