# installed
from fastapi import FastAPI
# local
from app.api import book, auth, user


app = FastAPI()


app.include_router(book.router)
app.include_router(auth.router)
app.include_router(user.router)