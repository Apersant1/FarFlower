
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from . import config
from .db import DB_INITIALIZER


from .routes import UserRouter

cfg: config.Config = config.load_config()


SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting")
    # await create_db_and_tables()
    yield
    print("Ending")
    
app = FastAPI(
    version='0.0.1',
    title='User-Service',
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)
app.include_router(UserRouter)
