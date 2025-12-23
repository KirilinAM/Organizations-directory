from typing import List

from fastapi import APIRouter, Depends

import app.api.activity.models as act
import app.api.organization.models as org
from app.api.activity.dao import ActivityDAO
from app.api.organization.dao import OrganizationDAO
from app.database.database import connection
from app.security import verifyApiKey


router = APIRouter(
    prefix="/v1/activities", tags=["Деятельность"], dependencies=[Depends(verifyApiKey)]
)


@router.get(
        "/", 
        summary="Получение деятельностей", 
        description="Получение всех деятельностей", 
        response_model=List[act.Activity]
)
async def getActivityByFilter(filterBy: act.ActivityFilter = Depends()):
    return await connection(ActivityDAO.findAll)(
        **filterBy.model_dump(exclude_none=True)
    )


@router.get(
    "/{id}",
    summary="Получение деятельности и её поддеятельностей по id",
    description="Получение деятельности и её поддеятельностей по id",
    response_model=act.ActivityWithDescendans,
)
async def getActivityById(id: int):
    return await connection(ActivityDAO.getItAndAllDescendans)(id=id)


@router.get(
    "/{id}/organizations",
    summary="Получение организаций по деятельности",
    description="Получение организаций ведущих указанную деятельность / её поддеятельности",
    response_model=List[org.Organization],
)
async def getOrganisationByActivityFamily(id: int):
    res = await connection(OrganizationDAO.findByActivityUpperId)(upperId=id)
    return res
