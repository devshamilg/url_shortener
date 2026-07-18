from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

