# base
from datetime import date
# installed
import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.models.book import Book, BorrowedBook
from app.models.reader import Reader
from app.services.book_service import BookService
from app.services.reader_service import ReaderService


@pytest.mark.asyncio
async def test_borrow_particular_book_reader_success(mocker):
    """ Тест успешной выдачи книги """
    mock_db = mocker.MagicMock(spec=AsyncSession)
    mock_db.commit = AsyncMock()

    book = Book(copies_quantity=1)

    reader = Reader(borrowed_books=[])

    # Мокаем сервисы
    book_service = BookService(mock_db)
    book_service.get_particular_book = AsyncMock(return_value=book)

    mock_reader_service = mocker.MagicMock(spec=ReaderService)
    mock_reader_service.get_particular_reader = AsyncMock(return_value=reader)
    mocker.patch('app.services.book_service.ReaderService', return_value=mock_reader_service)

    result = await book_service.borrow_particular_book_reader(book_id=1, reader_id=1)

    assert isinstance(result, BorrowedBook)
    assert book.copies_quantity == 0
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_borrow_book_no_copies_available(mocker):
    """ Тест случая, когда нет доступных экземпляров """
    mock_db = mocker.MagicMock()
    book = Book(copies_quantity=0)

    book_service = BookService(mock_db)
    book_service.get_particular_book = AsyncMock(return_value=book)

    with pytest.raises(ValueError, match="Нет доступных экземпляров данной книги"):
        await book_service.borrow_particular_book_reader(book_id=1, reader_id=1)


@pytest.mark.asyncio
async def test_borrow_book_already_borrowed(mocker):
    """ Тест случая, когда читатель уже взял эту книгу """
    mock_db = mocker.MagicMock()
    book = Book(id=1, copies_quantity=1)

    borrowed_book = BorrowedBook(book_id=1, reader_id=1)
    reader = Reader(id=1, borrowed_books=[borrowed_book])

    book_service = BookService(mock_db)
    book_service.get_particular_book = AsyncMock(return_value=book)

    mock_reader_service = mocker.MagicMock()
    mock_reader_service.get_particular_reader = AsyncMock(return_value=reader)
    mocker.patch('app.services.book_service.ReaderService', return_value=mock_reader_service)

    with pytest.raises(ValueError, match="Читатель уже брал эту книгу и еще не вернул"):
        await book_service.borrow_particular_book_reader(book_id=1, reader_id=1)


@pytest.mark.asyncio
async def test_borrow_book_max_limit_reached(mocker):
    """ Тест случая, когда читатель достиг лимита книг """
    mock_db = mocker.MagicMock()
    book = Book(id=1, copies_quantity=1)

    # Создаем читателя с 3 уже взятыми книгами
    borrowed_books = [
        BorrowedBook(book_id=2, reader_id=1),
        BorrowedBook(book_id=3, reader_id=1),
        BorrowedBook(book_id=4, reader_id=1)
    ]
    reader = Reader(id=1, borrowed_books=borrowed_books)

    book_service = BookService(mock_db)
    book_service.get_particular_book = AsyncMock(return_value=book)

    mock_reader_service = mocker.MagicMock()
    mock_reader_service.get_particular_reader = AsyncMock(return_value=reader)
    mocker.patch('app.services.book_service.ReaderService', return_value=mock_reader_service)

    with pytest.raises(ValueError, match="Читатель не может взять больше 3-х книг"):
        await book_service.borrow_particular_book_reader(book_id=1, reader_id=1)


@pytest.mark.asyncio
async def test_return_book_success(mocker):
    """ Тест успешного возврата книги """
    # Arrange
    mock_db = mocker.MagicMock()
    mock_db.scalar = AsyncMock()
    mock_db.commit = AsyncMock()

    borrowed_book = BorrowedBook(book_id=1, reader_id=1, is_active=True)

    book = Book(id=1, copies_quantity=0,)

    # Мокаем вызовы БД
    mock_db.scalar.return_value = borrowed_book

    book_service = BookService(mock_db)
    book_service.get_particular_book = AsyncMock(return_value=book)

    result = await book_service.return_particular_book_reader(book_id=1, reader_id=1)

    assert result == borrowed_book
    assert borrowed_book.is_active is False
    assert borrowed_book.return_date == date.today()
    assert book.copies_quantity == 1
    mock_db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_return_book_not_borrowed(mocker):
    """ Тест попытки вернуть книгу, которую читатель не брал """
    mock_db = mocker.MagicMock()
    mock_db.scalar = AsyncMock(return_value=None)

    book_service = BookService(mock_db)

    with pytest.raises(ValueError, match="Читатель не брал эту книгу или уже вернул ее"):
        await book_service.return_particular_book_reader(book_id=1, reader_id=1)


@pytest.mark.asyncio
async def test_return_book_already_returned(mocker):
    """ Тест попытки вернуть уже возвращенную книгу """
    mock_db = mocker.MagicMock()

    mock_db.scalar = AsyncMock(return_value=None)

    book_service = BookService(mock_db)

    with pytest.raises(ValueError, match="Читатель не брал эту книгу или уже вернул ее"):
        await book_service.return_particular_book_reader(book_id=1, reader_id=1)


@pytest.mark.asyncio
async def test_return_book_increments_quantity_correctly(mocker):
    """ Тест корректного увеличения количества книг """
    mock_db = mocker.AsyncMock()
    mock_db.scalar = AsyncMock(return_value=BorrowedBook(
        book_id=1,
        reader_id=1,
        is_active=True
    ))

    book = Book(
        id=1,
        copies_quantity=5
    )

    book_service = BookService(mock_db)
    book_service.get_particular_book = AsyncMock(return_value=book)

    await book_service.return_particular_book_reader(book_id=1, reader_id=1)

    assert book.copies_quantity == 6


@pytest.mark.asyncio
async def test_return_book_updates_return_date(mocker):
    """ Тест установки правильной даты возврата """
    mock_db = mocker.AsyncMock()
    borrowed_book = BorrowedBook(
        book_id=1,
        reader_id=1,
        is_active=True
    )
    mock_db.scalar = AsyncMock(return_value=borrowed_book)

    book_service = BookService(mock_db)
    book_service.get_particular_book = AsyncMock(return_value=Book(id=1, copies_quantity=0))

    await book_service.return_particular_book_reader(book_id=1, reader_id=1)

    assert borrowed_book.return_date == date.today()
    assert borrowed_book.is_active is False