# base
from typing import Annotated
# installed
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.models.librarian import Librarian
from app.services.dependencies import get_db_session
from app.services.book_service import BookService
from app.services.dependencies import get_current_user
from app.schemas.book import CreateBook, UpdateBook


router = APIRouter(prefix="/books", tags=["Book"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        librarian: Annotated[Librarian, Depends(get_current_user)]
):
    # БЕЗ JWT
    """ Получение всех книг """
    book_service = BookService(db)
    return await book_service.get_all_books()


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        book_id: int):
    """ Получение конкретной книги """
    book_service = BookService(db)
    try:
        book = await book_service.get_particular_book(book_id)
        return book
    except NoResultFound:
        raise HTTPException(
            detail="Книги с таким id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get("/reader/{reader_id}", status_code=status.HTTP_200_OK)
async def get_reader_books(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        reader_id: int
):
    """ Получение книг взятых читателем """
    book_service = BookService(db)
    try:
        borrowed_books = await book_service.get_reader_all_books(reader_id)
        return borrowed_books
    except NoResultFound:
        raise HTTPException(
            detail="Читателя с таким id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        book_data: CreateBook
):
    """ Создание книги """
    book_service = BookService(db)
    book = await book_service.create_particular_book(book_data)
    return book


@router.patch("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        book_id: int,
        book_data: UpdateBook):
    """ Обновление книги """
    book_service = BookService(db)
    try:
        await book_service.update_particular_book(book_id, book_data)
    except NoResultFound:
        raise HTTPException(
            detail="Книги с таким id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        book_id: int
):
    """ Удаление книги """
    book_service = BookService(db)
    try:
        await book_service.delete_particular_book(book_id)
    except NoResultFound:
        raise HTTPException(
            detail="Книги с таким id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/borrow/{book_id}/reader/{reader_id}", status_code=status.HTTP_201_CREATED)
async def borrow_book_reader(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        book_id: int,
        reader_id: int):
    """ Выдача книги читателю """
    book_service = BookService(db)
    try:
        borrow_book = await book_service.borrow_particular_book_reader(book_id, reader_id)
        return borrow_book
    except ValueError as error:
        raise HTTPException(
            detail=error.args[0],
            status_code=status.HTTP_409_CONFLICT
        )
    except NoResultFound:
        raise HTTPException(
            detail="Книги или пользователя с такими id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post("/return/{book_id}/reader/{reader_id}", status_code=status.HTTP_200_OK)
async def return_book_library(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        book_id: int,
        reader_id: int):
    """ Возврат книги от читателя в библиотеку """
    book_service = BookService(db)
    try:
        return_book = await book_service.return_particular_book_reader(book_id, reader_id)
        return return_book
    except ValueError as error:
        raise HTTPException(
            detail=error.args[0],
            status_code=status.HTTP_409_CONFLICT
        )
    except NoResultFound:
        raise HTTPException(
            detail="Книги или пользователя с такими id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )
