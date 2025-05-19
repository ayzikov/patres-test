# base
from typing import Annotated
# installed
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.services.dependencies import get_db_session
from app.services.reader_service import ReaderService
from app.services.librarian_service import LibrarianService
from app.services.auth_service import AuthService
from app.schemas.user import CreateReader, CreateLibrarian


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/registration/reader", status_code=status.HTTP_201_CREATED)
async def reader_registration(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        reader_data: CreateReader
):
    """ Регистрация читателя """
    reader_service = ReaderService(db)
    reader = await reader_service.create_particular_reader(reader_data)
    return reader


@router.post("/registration/librarian", status_code=status.HTTP_201_CREATED)
async def librarian_registration(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        librarian_data: CreateLibrarian
):
    """ Регистрация библиотекаря """
    librarian_service = LibrarianService(db)
    librarian = await librarian_service.create_particular_librarian(librarian_data)
    return librarian


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """ Авторизация """
    auth_service = AuthService(db)
    librarian_service = LibrarianService(db)
    try:
        librarian = await librarian_service.get_particular_librarian(form_data.username)
    except NoResultFound:
        raise HTTPException(
            detail="Библиотекаря с таким email не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    hashed_pass = librarian.password
    if not auth_service.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильная почта или пароль"
        )

    return {
        "access_token": auth_service.create_access_token(librarian.email),
        "refresh_token": auth_service.create_refresh_token(librarian.email),
    }