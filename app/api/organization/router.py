from fastapi import APIRouter,  Depends
import app.api.organization.models as org
import app.api.building.models as bld
import app.api.activity.models as act
from typing import List
from app.api.organization.dao import OrganizationDAO

router = APIRouter(prefix='/org',tags=['Работа с организациями'])


@router.get('/',summary="Получить все организации", response_model=List[org.Organization])
async def getAllOrganisation():
    return await OrganizationDAO.findAll()

@router.post('/',summary="Получить все организации c возможностью фильтрации", response_model=List[org.Organization])
async def getAllOrganisationByFilter(filterBy : org.OrganizationFilter):
    return await OrganizationDAO.findAll(**filterBy.toDict())

@router.get('/{id}',summary="Получить полную информациию об организации по id",response_model=org.OrganizationFullInfo | None)
async def getOrganisationById(id: int):
    return await OrganizationDAO.findFullData(id=id)

@router.post('/filter_by/building',summary="Получить организации с фильтром по полям здания",response_model=List[org.OrganizationFullInfo])
async def getOrganisationsByBuilding(filterBy: bld.BuildingFilter): 
    return await OrganizationDAO.findAllByBuilding(**filterBy.toDict())

@router.post('/filter_by/activity',summary="Получить организации с фильтром по полям деятельности",response_model=List[org.OrganizationFullInfo])
async def getOrganisationByActivity(filterBy: act.ActivityFilter): 
    return await OrganizationDAO.findAllByActivity(**filterBy.toDict())

@router.get('/filter_by/activity/{upperActivityId}',summary="Получить организации с активностью по id или её субоктивностями",response_model=List[org.OrganizationFullInfo])
async def getOrganisationByActivityFamily(upperActivityId: int): 
    return await OrganizationDAO.findAllByActivityUpperId(upperActivityId)

@router.post('/in_area',summary="Cписок организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте",response_model=List[org.Organization])
async def getOrganisationsInArea(inArea: bld.InArea):
    return await OrganizationDAO.findAllInArea(inArea)
