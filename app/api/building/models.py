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
    latitude: Latitude
    longitude: Longitude
    area: 'InRectangle | InCircle'
    
class InRectangle(BaseModel):
    half_height: float = Field(gt=0,description='Половина высоты прямоугольника в метрах')
    half_width: float = Field(gt=0,description='Половина ширины прямоугольника в метрах')

class InCircle(BaseModel):
    radius: float = Field(gt=0,description='Радиус окружности')