from pydantic import BaseModel, Field
from typing import List, Annotated

class Activity(BaseModel):
    id: int
    name: str


class ActivityTree(Activity):
    subactivity: List['Activity']