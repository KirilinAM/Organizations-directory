from sqlalchemy.future import select
from app.database.database import asyncSessionMaker

class BaseDAO:
    model = None

    @classmethod
    async def findAll(cls, **filter_by):
        async with asyncSessionMaker() as session:
            query = select(cls.model).filter_by(**filter_by)
            students = await session.execute(query)
            return students.scalars().all()
        
    @classmethod
    async def findOneOrNone(cls, **filter_by):
        async with asyncSessionMaker() as session:
            query = select(cls.model).filter_by(**filter_by)
            students = await session.execute(query)
            return students.scalars().one_or_none()
        