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
        usualFilterRes = await super().findAll(session, **filter_by)
        inAreaRes = await cls.findAllInArea(session, **filter_by)
        # union = select(usualFilterRes).join(inAreaRes)
        return usualFilterRes
    
    @classmethod 
    async def findAllInArea(cls, session: AsyncSession, **inArea):
        if isValidation(InCircle,**inArea):
            inCircle = InCircle(**inArea)
            res = await BuildingDAO.findAllInCircle(session=session,inCircle=inCircle)
        elif isValidation(InBox,**inArea):
            inBox = InBox(**inArea)
            res = await BuildingDAO.findAllInBox(session=session,inBox=inBox)
        else:
            res = []
        
        return res

    @classmethod
    async def findAllInCircle(cls, session: AsyncSession, inCircle: InCircle):
        pass

    
    @classmethod
    async def findAllInBox(cls, session: AsyncSession, inBox: InBox):
        pass

