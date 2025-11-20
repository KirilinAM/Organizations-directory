from fastapi import APIRouter,  Depends
import app.api.building.models as bld
from app.database.database import connection
from typing import List
from app.api.building.dao import BuildingDAO
from app.security import verifyApiKey

router = APIRouter(prefix='/v1/buildings',tags=['Здания'],dependencies=[Depends(verifyApiKey)])

@router.post('/',summary="Получение зданий", response_model=List[bld.Building])
async def getAllOrganisationByFilter(filterBy : bld.BuildingFilter):
    return await connection(BuildingDAO.findAll)(**filterBy.toDict())

@router.get('/{id}',summary="Получение здания по id",response_model=bld.Building | None)
async def getOrganisationById(id: int):
    return await connection(BuildingDAO.findAll)(id=id)

@router.get(
        '/filter_by/in_area'
        ,summary="Cписок организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте"
        ,response_model=List[List[bld.Building]]
)
async def getOrganisationsInArea(inArea: bld.InArea = Depends()):
    inAreaDict = inArea.model_dump() 
    res = []
    # if inArea.radius:
    #     inCircle = bld.InCircle(**inAreaDict)
    #     res = await connection(BuildingDAO.findAllInCircle)(inCircle)
    # else:
    #     inBox = bld.InBox(**inAreaDict)
    #     res = await connection(BuildingDAO.findAllInBox)(inBox)
    return res
