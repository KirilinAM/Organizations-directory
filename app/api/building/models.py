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

class InCircle(BaseModel):
    latitude: Latitude
    longitude: Longitude
    radius: float = Field(ge=0,description='Радиус окружности в км')

class InBox(BaseModel):
    latitude: Latitude 
    longitude: Longitude 
    bbox_latitude: float = Field(ge=0,description='Размах широты прямоугольника')
    bbox_longitude: float = Field(ge=0,description='Размах долготы прямоугольника')

def isValidation(model: Type[BaseModel], **data) -> bool:
    try:
        model(**data)
    except ValidationError:
        return False
    else:
        return True