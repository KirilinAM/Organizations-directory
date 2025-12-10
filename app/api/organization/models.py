from typing import List

from pydantic import BaseModel, ConfigDict

from app.api.activity.models import Activity
from app.api.building.models import Building


class Organization(BaseModel):
    id: int
    name: str
    building_id: int


class OrganizationFullInfo(Organization):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building_id: int
    phones: List["Phone"]
    building: "Building"
    activities: List["Activity"]


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
