from app.database.dao import BaseDAO
from app.database.models import Organization, Organization_Activity_Rel, Building
from app.database.database import asyncSessionMaker
import app.api.building.models as bld
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import func
from app.api.activity.dao import ActivityDAO
from geoalchemy2 import Geography

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
                .join(cls.model.activities)
                .filter_by(**filterBy)
                .distinct()
                .options(selectinload(cls.model.phones),joinedload(cls.model.building),selectinload(cls.model.activities))
            )
            result = await session.execute(query)
            result = result.scalars().all()
        return result
        
    @classmethod
    async def findAllByActivityUpperId(cls, upperId):
        activityCte = await ActivityDAO.getItAndAllDescendansIdCte(upperId)
        query = (
            select(cls.model)
            .join(Organization_Activity_Rel)
            .join(activityCte, activityCte.c.id == Organization_Activity_Rel.activity_id)
            .distinct()
            .options(selectinload(cls.model.phones),joinedload(cls.model.building),selectinload(cls.model.activities))
        )
        async with asyncSessionMaker() as session:
            result = await session.execute(query)
            result = result.scalars().all()
        return result

    @classmethod
    async def findAllInCircle(cls, circle: bld.InCircle):
        lat = circle.circle_latitude
        lng = circle.circle_longitude
        radius_km = circle.radius
        point = f'POINT({lng} {lat})'
        
        async with asyncSessionMaker() as session:
            query = (
                select(cls.model)
                .join(cls.model.building)
                .filter(
                    func.ST_DWithin(
                        Building.geom,
                        func.ST_GeogFromText(point),
                        radius_km * 1000  # конвертируем км в метры
                    )
                )
                .distinct()
                .options(selectinload(cls.model.phones),joinedload(cls.model.building),selectinload(cls.model.activities))
            )
            result = await session.execute(query)
            result = result.scalars().all()

            return result


    @classmethod
    async def findAllInBox(cls, box: bld.InBox):
        minLat = box.bbox_down
        maxLat = box.bbox_top
        minLng = box.bbox_left
        maxLng = box.bbox_right
        bbox = f'POLYGON(({minLng} {minLat}, {maxLat} {minLat}, {maxLat} {maxLng}, {minLng} {maxLng}, {minLng} {minLat}))'
       
        async with asyncSessionMaker() as session:
            query = (
                select(cls.model)
                .join(cls.model.building)
                .filter(
                    func.ST_Intersects(
                        Building.geom,
                        func.ST_GeogFromText(bbox)
                    )
                )
                .distinct()
                .options(selectinload(cls.model.phones),joinedload(cls.model.building),selectinload(cls.model.activities))
            )
            result = await session.execute(query)
            result = result.scalars().all()

            return result