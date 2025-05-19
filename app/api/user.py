# base
from typing import Annotated
# installed
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.services.dependencies import get_db_session
from app.schemas.user import UpdateReader
from app.services.reader_service import ReaderService


router = APIRouter(prefix="/users", tags=["User"])


@router.get("/readers")
async def get_readers(
        db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """ Получение всех читателей """
    reader_service = ReaderService(db)
    return await reader_service.get_all_readers()


@router.get("/readers/{reader_id}")
async def get_reader(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        reader_id: int
):
    """ Получение одного читателя """
    reader_service = ReaderService(db)
    try:
        await reader_service.get_particular_reader(reader_id)
    except NoResultFound:
        raise HTTPException(
            detail="Читателя с таким id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.patch("/readers/{reader_id}")
async def update_reader(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        reader_id: int,
        reader_data: UpdateReader
):
    """ Обновление одного читателя """
    reader_service = ReaderService(db)
    try:
        await reader_service.update_particular_reader(reader_id, reader_data)
    except NoResultFound:
        raise HTTPException(
            detail="Читателя с таким id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.patch("/readers/{reader_id}")
async def delete_reader(
        db: Annotated[AsyncSession, Depends(get_db_session)],
        reader_id: int,
):
    """ Удаление одного читателя """
    reader_service = ReaderService(db)
    try:
        await reader_service.delete_particular_reader(reader_id)
    except NoResultFound:
        raise HTTPException(
            detail="Читателя с таким id не существует",
            status_code=status.HTTP_400_BAD_REQUEST
        )
