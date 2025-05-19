# installed
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.models.librarian import Librarian
from app.schemas.user import CreateLibrarian
from app.services.auth_service import AuthService


class LibrarianService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_particular_librarian(self, librarian_data: CreateLibrarian):
        """ Создание библиотекаря """
        # хешируем пароль
        auth_service = AuthService(self.db)
        password = auth_service.hash_password(librarian_data.password)

        librarian = Librarian(
            name=librarian_data.name,
            email=librarian_data.email,
            password=password
        )
        self.db.add(librarian)
        await self.db.commit()
        return librarian


    async def get_particular_librarian(self, librarian_email: str):
        """ Получение библиотекаря """
        librarian = await self.db.scalar(select(Librarian).where(Librarian.email == librarian_email))
        if librarian is None:
            raise NoResultFound()
        return librarian
