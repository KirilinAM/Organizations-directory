from fastapi import APIRouter, Depends
import app.api.activity.models as act
from app.database.database import connection
from typing import List
from app.api.activity.dao import ActivityDAO
from app.security import verifyApiKey

router = APIRouter(prefix='/v1/activities',tags=['Деятельность'],dependencies=[Depends(verifyApiKey)])

@router.post('/',summary="Получение деятельностей", response_model=List[act.Activity])
async def getAllOrganisationByFilter(filterBy: act.ActivityFilter):
    return await connection(ActivityDAO.findAll)(**filterBy.toDict())

@router.get('/{id}',summary="Получение деятельности по id",response_model=act.Activity | None)
async def getOrganisationById(id: int):
    return await connection(ActivityDAO.findAll)(id=id)

@router.get(
        '/filter_by/activity/{upperActivityId}'
        ,summary="Получение поддеятельностей деятельности по id"
        ,response_model=List[act.Activity]
)
async def getOrganisationByActivityFamily(upperActivityId: int): 
    res = [] #await connection(OrganizationDAO.findAllByActivityUpperId)(upperActivityId)
    return res