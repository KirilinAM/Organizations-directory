from pydantic import BaseModel, Field, ConfigDict
from typing import List, Annotated

class Activity(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    parent_id: int

class ActivityFilter(BaseModel):
    name: str | None = None

    def toDict(self):
        return {key: val for key, val in self.model_dump().items() if val}