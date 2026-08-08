from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserRead, Token
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from app.models.user import User
from app.core.deps import require_roles

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    new_user = await auth_service.register(user_data)
    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate(form_data.username, form_data.password)

    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


