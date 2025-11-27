from pydantic import BaseModel, Field, ValidationError
from typing import Annotated, Type

Latitude = Annotated[float,Field(ge=-90,le=90,description='Широта')]
Longitude = Annotated[float,Field(ge=-180,le=180,description='Долгота')]

class Building(BaseModel):
    id: int
    address: str
    latitude: Latitude
    longitude: Longitude

class BuildingFilter(BaseModel):
    address: str | None = None
    latitude: Latitude | None = None
    longitude: Longitude | None = None
    radius: float | None = Field(default=None,gt=0,description='Радиус окружности в км. Взаимоисключающе с bbox_')
    bbox_latitude: Latitude | None = Field(default=None,description='Размах широты прямоугольника. Взаимоисключающе с radius')
    bbox_right: Longitude | None = Field(default=None,description='Размах долготы прямоугольника. Взаимоисключающе с radius')

class InCircle(BaseModel):
    latitude: Latitude
    longitude: Longitude
    radius: float = Field(gt=0,description='Радиус окружности в км')

class InBox(BaseModel):
    latitude: Latitude 
    longitude: Longitude 
    bbox_latitude: Latitude
    bbox_right: Longitude

def isValidation(model: Type[BaseModel], **data) -> bool:
    try:
        model(**data)
    except ValidationError:
        return False
    else:
        return True