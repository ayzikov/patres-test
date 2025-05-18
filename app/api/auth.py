# base
from typing import Annotated
# installed
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.backend.db_depends import get_db_session


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/reader", status_code=status.HTTP_201_CREATED)
async def reader_registration(db: Annotated[AsyncSession, Depends(get_db_session)]):
    """ Регистрация читателя """
    pass


@router.post("/librarian", status_code=status.HTTP_201_CREATED)
async def librarian_registration(db: Annotated[AsyncSession, Depends(get_db_session)]):
    """ Регистрация библиотекаря """
    pass