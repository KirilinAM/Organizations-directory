from fastapi import APIRouter,  Depends
import app.api.organization.models as org
import app.api.building.models as bld
import app.api.activity.models as act
from app.database.database import connection
from typing import List
from app.api.organization.dao import OrganizationDAO
from app.security import verifyApiKey

router = APIRouter(prefix='/v1/organizations',tags=['Организации'],dependencies=[Depends(verifyApiKey)])

@router.post('/',summary="Получение организаций", response_model=List[org.OrganizationFullInfo])
async def getAllOrganisationByFilter(filterBy : org.OrganizationFilter):
    return await connection(OrganizationDAO.findAll)(**filterBy.toDict())

@router.get('/{id}',summary="Получение организации по id",response_model=org.OrganizationFullInfo | None)
async def getOrganisationById(id: int):
    return await connection(OrganizationDAO.findFullData)(id=id)

