from sqlalchemy.ext.asyncio import AsyncSession
from app.database.dao import BaseDAO
from app.database.models import Building
from app.database.database import asyncSessionMaker
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.api.building.models import InCircle, InBox, isValidation

class BuildingDAO(BaseDAO):
    model = Building

    @classmethod
    async def findAll(cls, session: AsyncSession, **filter_by):
        return await super().findAll(session, **filter_by)
    
    @classmethod
    async def findAllInCircle(cls, session: AsyncSession, **inCircle):
        print('in circle')
        return []

    @classmethod
    async def findAllInBox(cls, session: AsyncSession, **inBox):
        print('in box')
        return []

