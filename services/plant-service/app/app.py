from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from . import config
from .db import DB_INITIALIZER, create_db_and_tables
from .routes import plant_router

cfg: config.Config = config.load_config()


SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting")
    #await create_db_and_tables()
    yield
    print("Ending")

app = FastAPI(
    version='0.0.1',
    title='Plant-Service',
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

app.include_router(plant_router)