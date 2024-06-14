import uuid
from typing import Optional, Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException


from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import Plant
from app.schemas import PlantReadSchemas, PlantCreateSchemas
from sqlalchemy.future import select
from jose.jwt import decode
from jose import JWTError
from app.config import Config, load_config


cfg: Config = load_config()

plant_router = APIRouter(
    prefix="/plants",
    tags=["plants"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_async_session)],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:5000/auth/jwt/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, cfg.SECRET, audience='fastapi-users:auth', algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError as e:
        raise e


# @plant_router.get("/", response_model=List[PlantReadSchemas])
# async def get_plants(db: AsyncSession = Depends(get_async_session)):
#     plants = await db.execute(select(Plant))
#     return plants



@plant_router.get("/test")
async def get_plants(db: AsyncSession = Depends(get_async_session),
                     user=Depends(get_current_user)):
    # теперь мы можем использовать информацию о пользователе для фильтрации растений
    """ plants = await db.execute(select(Plant).where(Plant.owner_id == user["user_id"])) """
    return user

""" @plant_router.get("/{plant_id}", response_model=PlantReadSchemas)
async def get_plant(plant_id: uuid.UUID,
                    db: AsyncSession = Depends(get_async_session)):
    plant = await db.execute(select(Plant).where(Plant.id == plant_id))
    plant = plant.scalars().first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant """