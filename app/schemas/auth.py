# base
from datetime import datetime
# installed
from pydantic import BaseModel


class TokenPayload(BaseModel):
    exp: datetime
    sub: str
    scope: str