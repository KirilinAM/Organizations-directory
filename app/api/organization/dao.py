from app.database.dao import BaseDAO
from app.database.models import Organization
from app.database.database import asyncSessionMaker
import app.api.building.models as bld
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

class OrganizationDAO(BaseDAO):
    model = Organization

    @classmethod
    async def findFullData(cls, id: int) -> dict | None:
        async with asyncSessionMaker() as session:
            # Запрос для получения информации о студенте вместе с информацией о факультете
            query = (
                select(cls.model)
                .options(joinedload(cls.model.phones),joinedload(cls.model.building),joinedload(cls.model.activities))
                .filter_by(id=id)
            )
            result = await session.execute(query)
            result = result.unique().scalar_one_or_none()

            # Если студент не найден, возвращаем None
            if not result:
                return None

            dictResult = result.toDict()
            dictResult['phones'] = [phone.toDict() for phone in result.phones]
            dictResult['building'] = result.building.toDict()
            dictResult['activities'] = [activity.toDict() for activity in result.activities]
            return dictResult
        
    @classmethod
    async def findAllByBuilding(cls, **filterBy):
        async with asyncSessionMaker() as session:
            query = select(cls.model).join(cls.model.building).filter_by(**filterBy)
            result = await session.execute(query)
            result = result.scalars().all()
            return [org.toDict() for org in result]
        
    @classmethod
    async def findAllByActivity(cls, **filterBy):
        async with asyncSessionMaker() as session:
            query = select(cls.model).join(cls.model.activities).filter_by(**filterBy)
            result = await session.execute(query)
            result = result.scalars().all()
            return [org.toDict() for org in result]
        
    @classmethod
    async def findAllInArea(cls, area: bld.InArea):
        pass