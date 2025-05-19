# base
import os
from datetime import datetime, timedelta, timezone
# installed
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt


load_dotenv()


class AuthService:
    def __init__(self, db):
        self.db = db
        self.UTC_3 = timezone(timedelta(hours=3))

        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 1  # 1 минута
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        self.JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

    def hash_password(self, password: str):
        """ Хэширует пароль """
        return self.bcrypt_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        """ Проверяет password на соответствие с hashed_password в БД """
        return self.bcrypt_context.verify(password, hashed_password)

    def create_access_token(self, subject: str):
        """ Создает access token """
        expires_delta = datetime.now(self.UTC_3) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "exp": expires_delta,
            "sub": subject,
            "scope": "access"
        }
        encoded_jwt = jwt.encode(payload, self.JWT_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, subject: str):
        """ Создает refresh token """
        expires_delta = datetime.now(self.UTC_3) + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)

        payload = {
            "exp": expires_delta,
            "sub": subject,
            "scope": "refresh"
        }
        encoded_jwt = jwt.encode(payload, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt
