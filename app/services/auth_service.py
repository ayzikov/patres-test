# installed
from passlib.context import CryptContext


class AuthService:
    def __init__(self):
        self.bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    async def hash_password(self, password: str):
        """ Метод хэширует пароль """
        return self.bcrypt_context.hash(password)

    async def verify_password(self, password: str, hashed_password: str):
        """ Проверяет password на соответствие с hashed_password в БД """
        return self.bcrypt_context.verify(password, hashed_password)
