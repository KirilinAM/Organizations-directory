from pydantic import BaseModel, Field
from typing import Annotated

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
    
    def toDict(self):
        return {key: val for key, val in self.model_dump().items() if val}
    
class InArea(BaseModel):
    circle_latitude: Latitude | None = Field(default=None,description='Широта центра окружности')
    circle_longitude: Longitude | None = Field(default=None,description='Долгота центра окружности')
    radius: float | None = Field(default=None,gt=0,description='Радиус окружности в км')
    bbox_down: Latitude | None = Field(default=None,description='Минимальная широта прямоугольника')
    bbox_top: Latitude | None = Field(default=None,description='Максимальная широта прямоугольника')
    bbox_left: Longitude | None = Field(default=None,description='Минимальная долгота прямоугольника')
    bbox_right: Longitude | None = Field(default=None,description='Максимальная долгота прямоугольника')
    

class InCircle(BaseModel):
    circle_latitude: Latitude = Field(description='Широта центра окружности')
    circle_longitude: Longitude= Field(description='Долгота центра окружности')
    radius: float= Field(gt=0,description='Радиус окружности в км')

class InBox(BaseModel):
    bbox_top: Latitude = Field(description='Максимальная широта прямоугольника')
    bbox_down: Latitude = Field(description='Минимальная широта прямоугольника')
    bbox_right: Longitude = Field(description='Максимальная долгота прямоугольника')
    bbox_left: Longitude = Field(description='Минимальная долгота прямоугольника')