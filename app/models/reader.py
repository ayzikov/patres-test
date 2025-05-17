# base
from typing import List
# installed
from sqlalchemy.orm import Mapped, relationship
# local
from app.models.user import BaseUser


class Reader(BaseUser):
    __tablename__ = "reader"

    borrowed_books: Mapped[List["BorrowedBook"]] = relationship(back_populates="reader")