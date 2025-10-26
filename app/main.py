from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def rootApi():
    return {'message': 'pass'}