# installed
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
# local
from app.models.reader import Reader
from app.schemas.user import CreateReader, UpdateReader
from app.services.other import model_to_dict


class ReaderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_particular_reader(self, reader_data: CreateReader):
        """ Создание читателя """
        reader = Reader(
            name=reader_data.name,
            email=reader_data.email
        )

        self.db.add(reader)
        await self.db.commit()
        return reader

    async def get_all_readers(self):
        """ Получение всех читателей """
        readers = await self.db.scalars(select(Reader))
        return readers.all()

    async def get_particular_reader(self, reader_id: int):
        """ Получение конкретного читателя """
        reader = await self.db.scalar(select(Reader).where(Reader.id == reader_id))
        if reader is None:
            raise NoResultFound()
        return reader

    async def update_particular_reader(self, reader_id: int, reader_data: UpdateReader):
        """ Обновление читателя """
        # получаем читателя, чтобы проверить его существование
        reader = await self.get_particular_reader(reader_id)
        # данные из запроса в виде dict
        reader_data_dict = dict(reader_data)
        # данные из БД в виде dict
        reader_db_dict = await model_to_dict(reader)

        # если в запросе какое-то поле имеет значение None, то оно остается без изменений
        # для этого значение поля, которое содержит None, заменяется значением этого поля из БД
        for key, value in reader_data_dict.items():
            if value is None:
                reader_data_dict[key] = reader_db_dict.get(key)

        stmt = (
            update(Reader)
            .where(Reader.id == reader_id)
            .values(**reader_data_dict)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete_particular_reader(self, reader_id: int):
        """ Удаление читателя """
        # получаем читателя, чтобы проверить на существование в БД
        reader = await self.get_particular_reader(reader_id)
        await self.db.execute(delete(Reader).where(Reader.id == reader_id))
        await self.db.commit()