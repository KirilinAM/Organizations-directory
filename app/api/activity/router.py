from fastapi import APIRouter,  Depends
import app.api.organization.models as org
import app.api.building.models as bld
import app.api.activity.models as act
from app.database.database import connection
from typing import List
from app.api.organization.dao import OrganizationDAO
from app.security import verifyApiKey

router = APIRouter(prefix='/v1/activities',tags=['Деятельность'],dependencies=[Depends(verifyApiKey)])


# @router.post('/filter_by/activity',summary="Получить организации с фильтром по полям деятельности",response_model=List[org.OrganizationFullInfo])
# async def getOrganisationByActivity(filterBy: act.ActivityFilter): 
#     return await connection(OrganizationDAO.findAllByActivity)(**filterBy.toDict())

# @router.get('/filter_by/activity/{upperActivityId}',summary="Получить организации с активностью по id или её субоктивностями",response_model=List[org.OrganizationFullInfo])
# async def getOrganisationByActivityFamily(upperActivityId: int): 
#     return await connection(OrganizationDAO.findAllByActivityUpperId)(upperActivityId)