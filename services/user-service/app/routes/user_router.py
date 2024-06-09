import uuid
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from app.schemas import UserRead, UserCreate, UserUpdate

from app.auth.auth import AuthInitializer

from app.manager import get_user_manager
from app.db.userDB import User

from app.config import Config,load_config


cfg: Config = load_config()

UserRouter = APIRouter()

auth = AuthInitializer()
auth.initializer(cfg.SECRET)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager,
                                              [auth.auth_backend])

current_active_user = fastapi_users.current_user(active=True)

UserRouter.include_router(
    fastapi_users.get_auth_router(auth.auth_backend), prefix="/auth/jwt", tags=["auth"]
)
UserRouter.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
UserRouter.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
UserRouter.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
UserRouter.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
