from fastapi import FastAPI
from app.database.database import asyncSessionMaker
from sqlalchemy import text

app = FastAPI()

@app.get("/")
async def rootApi():
    async with asyncSessionMaker() as session:
        dbRes = await session.execute(text('SELECT 1'))
        dbRes = dbRes.scalar()
    return {'message': 'pass', 'db': dbRes}