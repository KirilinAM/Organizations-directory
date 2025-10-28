from pydantic import BaseModel, Field
from typing import Annotated

lattitude = Annotated[float,Field(ge=-90,le=90)]
longitude = Annotated[float,Field(ge=-180,le=180)]

class Building(BaseModel):
    id: int
    address: str
    latitude: lattitude
    longitude: longitude
