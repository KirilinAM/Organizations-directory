from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import connection

class BaseDAO:
    model = None

    @classmethod
    @connection
    async def findAll(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()
        
    @classmethod
    @connection
    async def findOneOrNone(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().one_or_none()
    