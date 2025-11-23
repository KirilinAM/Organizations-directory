from fastapi import APIRouter, Depends
import app.api.activity.models as act
from app.database.database import connection
from typing import List
from app.api.activity.dao import ActivityDAO
from app.security import verifyApiKey

router = APIRouter(prefix='/v1/activities',tags=['Деятельность'],dependencies=[Depends(verifyApiKey)])

@router.get('/',summary="Получение деятельностей", response_model=List[act.Activity])
async def getAllOrganisationByFilter(filterBy: act.ActivityFilter = Depends()):
    return await connection(ActivityDAO.findAll)(**filterBy.model_dump(exclude_none=True))

@router.get('/{id}',summary="Получение деятельности по id и её поддеятельностей",response_model=act.Activity | None)
async def getOrganisationById(id: int):
    return await connection(ActivityDAO.findOneOrNone)(id=id)

@router.get(
        '/{id}/organizations'
        ,summary="Получение организаций ведущих указанную деятельность / её поддеятельности"
        ,response_model=List[act.Activity]
)
async def getOrganisationByActivityFamily(id: int): 
    res = [] #await connection(OrganizationDAO.findAllByActivityUpperId)(upperActivityId)
    return res