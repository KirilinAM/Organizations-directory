from typing import List

from fastapi import APIRouter, Depends

import app.api.building.models as bld
import app.api.organization.models as org
from app.api.organization.dao import OrganizationDAO
from app.database.database import connection
from app.security import verifyApiKey


router = APIRouter(
    prefix="/v1/organizations",
    tags=["Организации"],
    dependencies=[Depends(verifyApiKey)],
)


@router.get(
    "/",
    summary="Получение организаций",
    # description="Получение всех организаций",
    response_model=List[org.Organization],
)
async def getAllOrganisationByFilter(filterBy: org.OrganizationFilter = Depends()):
    """Получение всех организаций"""
    return await connection(OrganizationDAO.findAll)(**filterBy.model_dump(exclude_none=True))


@router.get(
    "/in_circle",
    summary="Получение организаций в радиусе",
    description="Получение организаций в зданиях, которые находятся в заданном радиусе относительно указанной точки",
    response_model=List[org.Organization],
)
async def getOrganisationsInCircle(inCircle: bld.InCircle = Depends()):
    return await connection(OrganizationDAO.findByBuildingInCircle)(**inCircle.model_dump(exclude_none=True))


@router.get(
    "/in_box",
    summary="Получение организаций в прямоугольной области",
    description="Получение организаций в зданиях, которые находятся в заданной прямоугольной области относительно указанной точки",
    response_model=List[org.Organization],
)
async def getOrganisationsInBox(inBox: bld.InBox = Depends()):
    return await connection(OrganizationDAO.findByBuildingInBox)(**inBox.model_dump(exclude_none=True))


@router.get(
    "/by_activity_tree",
    summary="Получение организаций по деятельности",
    description="Получение организаций ведущих указанную деятельность / её поддеятельности",
    response_model=List[org.Organization],
)
async def getOrganisationByActivityFamily(upper_id: int):
    res = await connection(OrganizationDAO.findByActivityUpperId)(upperId=upper_id)
    return res


@router.get(
    "/{id}",
    summary="Получение организации по id",
    description="Получение организации по id",
    response_model=org.OrganizationFullInfo | None,
)
async def getOrganisationById(id: int):
    return await connection(OrganizationDAO.findFullData)(id=id)
