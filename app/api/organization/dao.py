from app.database.dao import BaseDAO
from app.database.models import Organization, Organization_Activity_Rel, Building
import app.api.building.models as bld
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.activity.dao import ActivityDAO
from geoalchemy2 import Geography
from app.api.activity.dao import ActivityDAO
from app.api.building.dao import BuildingDAO

class OrganizationDAO(BaseDAO):
    model = Organization

    @classmethod
    async def findFullData(cls, id: int, session: AsyncSession):
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
    async def findByBuildingId(cls, session: AsyncSession, **filterBy):
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
    async def findByActivityUpperId(cls, upperId: int, session: AsyncSession):
        activityCte = await ActivityDAO.getItAndAllDescendansIdCte(upperId)
        query = (
            select(cls.model)
            .join(Organization_Activity_Rel)
            .join(activityCte, activityCte.c.id == Organization_Activity_Rel.activity_id)
            .distinct()
        )

        result = await session.execute(query)
        result = result.scalars().all()

        return result

    @classmethod
    async def findByBuildingInCircle(cls, session: AsyncSession, **inCircle):
        buildings = await BuildingDAO.findAllInCircle(session=session,**inCircle)
        ids = [building.id for building in buildings]
        query = (
            select(cls.model)
            .filter(cls.model.building_id.in_(ids))
        )

        result = await session.execute(query)
        result = result.scalars().all()

        return result

    @classmethod
    async def findByBuildingInBox(cls, session: AsyncSession, **inBox):
        buildings = await BuildingDAO.findAllInBox(session=session,**inBox)
        ids = [building.id for building in buildings]
        query = (
            select(cls.model)
            .filter(cls.model.building_id.in_(ids))
        )

        result = await session.execute(query)
        result = result.scalars().all()

        return result
