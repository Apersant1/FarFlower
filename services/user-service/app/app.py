import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware
from . import config
from .db import DB_INITIALIZER, create_db_and_tables, User
from .auth import AuthInitializer
from .schemas import UserRead, UserCreate, UserUpdate
from .manager import get_user_manager




cfg: config.Config = config.load_config()


SessionLocal = DB_INITIALIZER.init_database(str(cfg.postgres_dsn))
auth = AuthInitializer()
auth.initializer(cfg.SECRET)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager,
                                              [auth.auth_backend])

current_active_user = fastapi_users.current_user(active=True)


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

app.include_router(
    fastapi_users.get_auth_router(auth.auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
