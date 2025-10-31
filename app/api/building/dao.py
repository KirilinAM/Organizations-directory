from app.database.dao import BaseDAO
from app.database.models import Building
from app.database.database import asyncSessionMaker
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

class BuildingDAO(BaseDAO):
    model = Building
