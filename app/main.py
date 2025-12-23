from fastapi import FastAPI
from sqlalchemy import text

from app.api.activity.router import router as actRouter
from app.api.building.router import router as bldRouter
from app.api.organization.router import router as orgRouter


app = FastAPI()
app.include_router(orgRouter)
app.include_router(actRouter)
app.include_router(bldRouter)


@app.get("/")
async def rootApi():
    return {"message": "online"}
