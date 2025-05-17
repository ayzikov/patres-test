# installed
from email_validator import validate_email
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates
# local
from app.backend.db import Base


class BaseUser(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(unique=True)

    @validates("email")
    def email_validate(self, key, address):
        if not validate_email(address):
            raise ValueError("Некорректный адрес электронной почты")
        return address
