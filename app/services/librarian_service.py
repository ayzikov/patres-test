# installed
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.models.librarian import Librarian
from app.schemas.user import CreateLibrarian


class LibrarianService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    async def create_particular_librarian(self, librarian_data: CreateLibrarian):
        """ Создание библиотекаря """
        librarian = Librarian(
            name=librarian_data.name,
            email=librarian_data.email,
            password=self.bcrypt_context.hash(librarian_data.password)
        )
        self.db.add(librarian)
        await self.db.commit()
        return librarian
