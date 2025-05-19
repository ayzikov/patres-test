# installed
from pydantic import ValidationError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.backend.db import async_session_maker
from app.schemas.auth import TokenPayload
from app.services.librarian_service import LibrarianService
from app.services.auth_service import AuthService


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)):
    """ Зависимость для авторизации библиотекаря """
    db = Depends(get_db_session)
    auth_service = AuthService(db)
    librarian_service = LibrarianService(db)

    try:
        payload = jwt.decode(
            token=token,
            key=auth_service.JWT_SECRET_KEY,
            algorithms=[auth_service.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен истек",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не удалось проверить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    librarian = await librarian_service.get_particular_librarian(token_data.sub)
    return librarian


async def get_db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session