from pydantic import BaseModel, Field, ConfigDict
from typing import List, Annotated

class Activity(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    parent_id: int | None

class ActivityFilter(BaseModel):
    name: str | None = None

class ActivityWithDescendans(Activity):
    # model_config = ConfigDict(from_attributes=True)

    descendans: List[Activity]