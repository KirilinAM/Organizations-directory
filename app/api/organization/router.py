from fastapi import APIRouter,  Depends
import app.api.organization.models as org
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

# @router.post('/filter_by',summary="Список организаций по фильтрам: Название, Здание, Деятельность")
# async def getOrganisationByName(filter: OrganisationsFilterRequest) -> OrganisationsIdFiltredResponce:
#     return OrganisationsIdFiltredResponce()

# @router.post('/in_area',summary="Cписок организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте")
# async def getOrganisationsByBuilding(inArea: OrganisationsInAreaRequest) -> OrganisationsIdInAreaResponce:
#     return OrganisationsIdInAreaResponce()
