from pydantic import BaseModel, Field, ConfigDict
from typing import List, Annotated
from app.api.building.models import *
from app.api.activity.models import *


class Organization(BaseModel):
    id: int
    name: str
    building_id: int

class OrganizationFullInfo(Organization):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    building_id: int
    phones: List['Phone']
    building: 'Building'
    activities: List['Activity']

class Phone(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    number: str

    # @field_validator("number")
    # def checkPhone(cls, value):
    #     if not re.match(r'^\+\d{1,15}$', value):
    #         raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
    #     return value

class OrganizationFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = None
    building_id: int | None = None

    def toDict(self):
        return {key: val for key, val in self.model_dump().items() if val}