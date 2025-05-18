# installed
from sqlalchemy import inspect


async def model_to_dict(model):
    """ Функция преобразует экземпляр модели в словарь python """
    inspector = inspect(model)
    return {attr.key: getattr(model, attr.key) for attr in inspector.mapper.column_attrs}
