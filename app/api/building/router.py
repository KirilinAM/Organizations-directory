from typing import List

from fastapi import APIRouter, Depends

import app.api.building.models as bld
from app.api.building.dao import BuildingDAO
from app.database.database import connection
from app.security import verifyApiKey


router = APIRouter(
    prefix="/v1/buildings", tags=["Здания"], dependencies=[Depends(verifyApiKey)]
)


@router.get(
    "/", 
    summary="Получение зданий", 
    description="Получение всех зданий", 
    response_model=List[bld.Building]
)
async def getAllOrganisationByFilter(filterBy: bld.BuildingFilter = Depends()):
    return await connection(BuildingDAO.findAll)(
        **filterBy.model_dump(exclude_none=True)
    )


@router.get(
    "/in_circle",
    summary="Получение зданий в радиусе",
    description="Получение зданий, которые находятся в заданном радиусе относительно указанной точки",
    response_model=List[bld.Building],
)
async def getBuildingsInCircle(inCircle: bld.InCircle = Depends()):
    return await connection(BuildingDAO.findAllInCircle)(
        **inCircle.model_dump(exclude_none=True)
    )


@router.get(
    "/in_box",
    summary="Получение зданий в прямоугольной области",
    description="Получение зданий, которые находятся в заданной прямоугольной области относительно указанной точки",
    response_model=List[bld.Building],
)
async def getBuildingsInBox(inBox: bld.InBox = Depends()):
    return await connection(BuildingDAO.findAllInBox)(
        **inBox.model_dump(exclude_none=True)
    )


@router.get(
    "/{id}", 
    summary="Получение здания по id", 
    description="Получение здания по id", 
    response_model=bld.Building | None
)
async def getBuildingsById(id: int):
    return await connection(BuildingDAO.findOneOrNone)(id=id)
