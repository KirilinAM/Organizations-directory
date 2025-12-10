from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class BaseDAO:
    model = None

    @classmethod
    async def findAll(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def findOneOrNone(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().one_or_none()
