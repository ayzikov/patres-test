# base
import datetime
from typing import List, Optional
# installed
from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.backend.db import Base


class Book(Base):
    __tablename__ = "book"
    __table_args__ = (
        CheckConstraint("copies_quantity >= 0", name="check_book_copies_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    publication_year: Mapped[Optional[int]] = mapped_column()
    isbn: Mapped[Optional[str]] = mapped_column(String(13), unique=True)
    copies_quantity: Mapped[int] = mapped_column(default=1)
    description: Mapped[str] = mapped_column(String(500))

    borrowed_books: Mapped[List["BorrowedBook"]] = relationship(back_populates="book")


class BorrowedBook(Base):
    __tablename__ = "borrowed_book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    borrow_date: Mapped[datetime.date] = mapped_column(default=datetime.date.today())
    return_date: Mapped[Optional[datetime.date]] = mapped_column(nullable=True, default=None)
    is_active: Mapped[bool] = mapped_column(default=True)

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    book: Mapped["Book"] = relationship(back_populates="borrowed_books")

    reader_id: Mapped[int] = mapped_column(ForeignKey("reader.id"))
    reader: Mapped["Reader"] = relationship(back_populates="borrowed_books")



