# base
from typing import Optional
# installed
from pydantic import BaseModel


class CreateBook(BaseModel):
    name: str
    author: str
    publication_year: Optional[int] = None
    isbn: Optional[str] = None


class UpdateBook(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    copies_quantity: Optional[int] = None