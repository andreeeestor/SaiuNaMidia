from fastapi import APIRouter, Form, HTTPException, status
from core.config import settings
from core.security import create_access_token
from schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=TokenResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    if username.strip() == settings.AUTH_USER and password == settings.AUTH_PASSWORD:
        token = create_access_token({"sub": username.strip()})
        return TokenResponse(access_token=token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário ou senha inválidos",
    )
