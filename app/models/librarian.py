# base
import datetime
from typing import List, Optional
# installed
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.models.user import BaseUser


class Librarian(BaseUser):
    __tablename__ = "librarian"

    password: Mapped[str] = mapped_column()