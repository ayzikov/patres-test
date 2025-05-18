# base
from typing import Annotated
# installed
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.backend.db_depends import get_db_session


router = APIRouter(prefix="/books", tags=["Book"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(db: Annotated[AsyncSession, Depends(get_db_session)]):
    # БЕЗ JWT
    """ Получение всех книг """
    pass


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_book(db: Annotated[AsyncSession, Depends(get_db_session)], id: int):
    """ Получение конкретной книги """
    pass


@router.get("/reader/{id}", status_code=status.HTTP_200_OK)
async def get_reader_books(db: Annotated[AsyncSession, Depends(get_db_session)], id: int):
    """ Получение книг взятых читателем """
    pass


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(db: Annotated[AsyncSession, Depends(get_db_session)]):
    """ Создание книги """
    pass


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_book(db: Annotated[AsyncSession, Depends(get_db_session)], id: int):
    """ Обновление книги """
    pass


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_book(db: Annotated[AsyncSession, Depends(get_db_session)], id: int):
    """ Удаление книги """
    pass


@router.post("/{book_id}/reader/{reader_id}", status_code=status.HTTP_201_CREATED)
async def borrow_book_reader(db: Annotated[AsyncSession, Depends(get_db_session)], book_id: int, reader_id: int):
    """ Выдача книги читателю """
    pass


@router.post("/{book_id}/reader/{reader_id}", status_code=status.HTTP_200_OK)
async def return_book_library(db: Annotated[AsyncSession, Depends(get_db_session)], book_id: int, reader_id: int):
    """ Возврат книги от читателя в библиотеку """
    pass
