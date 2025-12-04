from sqlalchemy.ext.asyncio import AsyncSession
from app.database.dao import BaseDAO
from app.database.models import Building
from app.database.database import asyncSessionMaker
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from app.api.building.models import InCircle, InBox, isValidation

class BuildingDAO(BaseDAO):
    model = Building

    @classmethod
    async def findAll(cls, session: AsyncSession, **filter_by):
        return await super().findAll(session, **filter_by)
    
    @classmethod
    async def findAllInCircle(cls, session: AsyncSession, **inCircle):
        lng = inCircle['longitude']
        lat = inCircle['latitude']
        radiusKm = inCircle['radius']
        point = f'POINT({lng} {lat})'
        
        query = (
            select(cls.model)
            .filter(
                func.ST_DWithin(
                    Building.geom,
                    func.ST_GeogFromText(point),
                    radiusKm * 1000  # конвертируем км в метры
                )
            )
        )
        result = await session.execute(query)
        result = result.scalars().all()

        return result


    @classmethod
    async def findAllInBox(cls, session: AsyncSession, **inBox):
        lng = inBox['longitude']
        lat = inBox['latitude']
        bboxLng = inBox['bbox_longitude']
        bboxLat = inBox['bbox_latitude']

        minLng = lng - bboxLng / 2
        maxLng = lng + bboxLng / 2
        minLat = lat - bboxLat / 2
        maxLat = lat + bboxLat / 2
        bbox = f'POLYGON(({minLng} {minLat}, {minLng} {maxLat}, {maxLng} {maxLat}, {maxLng} {minLat}, {minLng} {minLat}))'
        query = (
            select(cls.model)
            .filter(
                func.ST_Intersects(
                    Building.geom,
                    func.ST_GeogFromText(bbox)
                )
            )
        )
        result = await session.execute(query)
        result = result.scalars().all()

        return result
