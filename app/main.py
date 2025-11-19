from fastapi import FastAPI
from app.database.database import asyncSessionMaker
from sqlalchemy import text
from app.api.organization.router import router as orgRouter
from app.api.activity.router import router as actRouter
from app.api.building.router import router as bldRouter

app = FastAPI()
app.include_router(orgRouter)
app.include_router(actRouter)
app.include_router(bldRouter)

@app.get("/")
async def rootApi():
    async with asyncSessionMaker() as session:
        dbRes = await session.execute(text('SELECT 1'))
        dbRes = dbRes.scalar()
    return {'message': 'pass', 'db': dbRes}