# base
import datetime
# installed
from sqlalchemy import select, delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

# local
from app.models.book import Book, BorrowedBook
from app.schemas.book import CreateBook, UpdateBook
from app.services.other import model_to_dict
from app.services.reader_service import ReaderService


class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self):
        """ Получение всех книг """
        books = await self.db.scalars(select(Book))
        return books.all()

    async def get_particular_book(self, book_id: int):
        """ Получение конкретной книги """
        book = await self.db.scalar(select(Book).where(Book.id == book_id))
        if book is None:
            raise NoResultFound()
        return book

    async def get_reader_all_books(self, reader_id: int):
        """ Получение книг взятых читателем, которые он не вернул"""
        # проверка на существование читателя
        reader_service = ReaderService(self.db)
        reader = await reader_service.get_particular_reader(reader_id)

        stmt = (select(BorrowedBook)
                .where(BorrowedBook.reader_id == reader_id)
                .where(BorrowedBook.is_active == True))
        borrowed_books = await self.db.scalars(stmt)
        return borrowed_books.all()

    async def create_particular_book(self, book_data: CreateBook):
        """ Создание книги """
        book = Book(
            name=book_data.name,
            author=book_data.author,
            publication_year=book_data.publication_year,
            isbn=book_data.isbn
        )

        self.db.add(book)
        await self.db.commit()
        return book

    async def update_particular_book(self, book_id: int, book_data: UpdateBook):
        """ Обновление книги """
        # получаем книгу, чтобы проверить ее на существование в БД
        book = await self.get_particular_book(book_id)
        # данные из запроса в виде dict
        book_data_dict = dict(book_data)
        # данные из БД в виде dict
        book_db_dict = await model_to_dict(book)

        # если в запросе какое-то поле имеет значение None, то оно остается без изменений
        # для этого значение поля, которое содержит None, заменяется значением этого поля из БД
        for key, value in book_data_dict.items():
            if value is None:
                book_data_dict[key] = book_db_dict.get(key)

        stmt = (
            update(Book)
            .where(Book.id == book_id)
            .values(**book_data_dict)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete_particular_book(self, book_id: int):
        """ Удаление книги """
        # получаем книгу, чтобы проверить ее на существование в БД
        book = await self.get_particular_book(book_id)
        await self.db.execute(delete(Book).where(Book.id == book_id))
        await self.db.commit()

    async def borrow_particular_book_reader(self, book_id: int, reader_id: int):
        """ Выдача книги читателю """
        # проверка количества экземпляров книги
        book = await self.get_particular_book(book_id)
        if book.copies_quantity <= 0:
            raise ValueError("Нет доступных экземпляров данной книги")

        reader_service = ReaderService(self.db)
        reader = await reader_service.get_particular_reader(reader_id)
        borrowed_books = reader.borrowed_books

        # проверка на то что читатель еще не взял эту книгу
        for reader_borrowed_book in borrowed_books:
            if reader_borrowed_book.book_id == book_id:
                raise ValueError("Читатель уже брал эту книгу и еще не вернул")

        # проверка на то что у читателя взято не больше 2-х книг
        if len(borrowed_books) >= 3:
            raise ValueError("Читатель не может взять больше 3-х книг")

        # создание BorrowedBook
        borrowed_book = BorrowedBook(
            book_id=book_id,
            reader_id=reader_id
        )
        self.db.add(borrowed_book)

        # убираем у книги экземпляр, который забрал читатель
        book.copies_quantity -= 1

        await self.db.commit()
        return borrowed_book

    async def return_particular_book_reader(self, book_id: int, reader_id: int):
        """ Возврат книги от читателя в библиотеку """
        # Проверяем есть ли borrowed_book, которую не вернул этот читатель
        stmt = (select(BorrowedBook)
                .where(BorrowedBook.book_id == book_id)
                .where(BorrowedBook.reader_id == reader_id)
                .where(BorrowedBook.is_active == True))
        borrow_book = await self.db.scalar(stmt)
        if borrow_book is None:
            raise ValueError("Читатель не брал эту книгу или уже вернул ее")

        # возвращаем
        borrow_book.is_active = False
        borrow_book.return_date = datetime.date.today()

        # прибавляем к экземплярам книги + 1
        book = await self.get_particular_book(book_id)
        book.copies_quantity += 1

        await self.db.commit()
        return borrow_book
