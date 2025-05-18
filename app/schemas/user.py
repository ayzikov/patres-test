# base
from typing import Optional
# installed
from pydantic import BaseModel


class BaseCreateUser(BaseModel):
    name: str
    email: str


class CreateReader(BaseCreateUser):
    pass


class UpdateReader(BaseCreateUser):
    name: Optional[str]
    email: Optional[str]


class CreateLibrarian(BaseCreateUser):
    password: str
