from fastapi import FastAPI, Depends

from app.auth.jwt_bearer import JWTBearer
from app.config import initiate_database
from app.routes import admin
from app.routes import student

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/ping", tags=["Ping"])
async def read_root():
    return {"message": "ok"}


app.include_router(admin.router, tags=["Administrator"], prefix="/admin")
app.include_router(student.router, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)], )
