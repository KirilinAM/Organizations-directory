from pydantic import BaseModel, Field
from typing import List, Annotated

class Activity(BaseModel):
    id: int
    name: str

class ActivityTree(Activity):
    subactivity: List['Activity']

class ActivityFilter(BaseModel):
    name: str | None = None

    def toDict(self):
        return {key: val for key, val in self.model_dump().items() if val}