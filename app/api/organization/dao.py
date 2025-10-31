from app.database.dao import BaseDAO
from app.database.models import Organization
from app.database.database import asyncSessionMaker
import app.api.building.models as bld
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import Select

class OrganizationDAO(BaseDAO):
    model = Organization

    @classmethod
    async def findFullData(cls, id: int):
        async with asyncSessionMaker() as session:
            query = (
                select(cls.model)
                .filter_by(id=id)
                .distinct()
                .options(selectinload(cls.model.phones),joinedload(cls.model.building),selectinload(cls.model.activities))
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()

            return result
        
    @classmethod
    async def findAllByBuilding(cls, **filterBy):
        async with asyncSessionMaker() as session:
            query = (
                select(cls.model)
                .join(cls.model.building)
                .filter_by(**filterBy)
                .distinct()
                .options(selectinload(cls.model.phones),joinedload(cls.model.building),selectinload(cls.model.activities))
            )
            result = await session.execute(query)
            result = result.scalars().all()

            return result
        
    @classmethod
    async def findAllByActivity(cls, **filterBy):
        async with asyncSessionMaker() as session:
            query = (
                select(cls.model)
                .join(cls.model.building)
                .filter_by(**filterBy)
                .distinct()
                .options(selectinload(cls.model.phones),joinedload(cls.model.building),selectinload(cls.model.activities))
            )
            result = await session.execute(query)
            result = result.scalars().all()
            return result
        
    @classmethod
    async def findAllInArea(cls, area: bld.InArea):
        pass