from fastapi import APIRouter,  Depends
import app.api.organization.models as org
import app.api.building.models as bld
import app.api.activity.models as act
from app.database.database import connection
from typing import List
from app.api.organization.dao import OrganizationDAO
from app.security import verifyApiKey

router = APIRouter(prefix='/v1/buildings',tags=['Здания'],dependencies=[Depends(verifyApiKey)])

# @router.post('/filter_by/building',summary="Получить организации с фильтром по полям здания",response_model=List[org.OrganizationFullInfo])
# async def getOrganisationsByBuilding(filterBy: bld.BuildingFilter): 
#     return await connection(OrganizationDAO.findAllByBuilding)(**filterBy.toDict())

# @router.get('/filter_by/in_area',summary="Cписок организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте",response_model=List[org.OrganizationFullInfo])
# async def getOrganisationsInArea(inArea: bld.InArea = Depends()):
#     inAreaDict = inArea.model_dump() 
#     res = []
#     if inArea.radius:
#         inCircle = bld.InCircle(**inAreaDict)
#         res = await connection(OrganizationDAO.findAllInCircle)(inCircle)
#     else:
#         inBox = bld.InBox(**inAreaDict)
#         res = await connection(OrganizationDAO.findAllInBox)(inBox)
#     return res
