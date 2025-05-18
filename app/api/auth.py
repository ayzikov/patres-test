# base
from typing import Annotated
# installed
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.backend.db_depends import get_db_session
from app.services.reader_service import ReaderService
from app.services.librarian_service import LibrarianService
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
