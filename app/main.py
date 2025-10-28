from fastapi import FastAPI
from app.database.database import asyncSessionMaker
from sqlalchemy import text
from app.api.organization.router import router as orgRouter

app = FastAPI()
app.include_router(orgRouter)

@app.get("/")
async def rootApi():
    async with asyncSessionMaker() as session:
        dbRes = await session.execute(text('SELECT 1'))
        dbRes = dbRes.scalar()
    return {'message': 'pass', 'db': dbRes}