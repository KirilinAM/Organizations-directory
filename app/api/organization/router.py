from fastapi import APIRouter,  Depends
import app.api.organization.models as org
import app.api.building.models as bld
import app.api.activity.models as act
from typing import List
from app.api.organization.dao import OrganizationDAO

router = APIRouter(prefix='/org',tags=['Работа с организациями'])


@router.get('/',summary="Получить все организации")
async def getAllOrganisation() -> List[org.Organization]:
    return await OrganizationDAO.findAll()

@router.post('/',summary="Получить все организации c возможностью фильтрации")
async def getAllOrganisation(filterBy : org.OrganizationFilter) -> List[org.Organization]:
    return await OrganizationDAO.findAll(**filterBy.toDict())

@router.get('/{id}',summary="Получить полную информациию об организации по id")
async def getOrganisationById(id: int) -> org.OrganizationFullInfo | None:
    return await OrganizationDAO.findFullData(id=id)

@router.post('/filter_by/building',summary="Получить организации с фильтром по полям здания")
async def getOrganisationByName(filterBy: bld.BuildingFilter) -> List[org.Organization]: 
    return await OrganizationDAO.findAllByBuilding(**filterBy.toDict())

@router.post('/filter_by/activity',summary="Получить организации с фильтром по полям деятельности")
async def getOrganisationByName(filterBy: act.ActivityFilter) -> List[org.Organization]: 
    return await OrganizationDAO.findAllByActivity(**filterBy.toDict())

@router.post('/in_area',summary="Cписок организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте")
async def getOrganisationsByBuilding(inArea: bld.InArea) -> List[org.Organization]:
    return await OrganizationDAO.findAllInArea(inArea)
