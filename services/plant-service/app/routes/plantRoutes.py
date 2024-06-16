import uuid
from typing import Optional, List, Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from httpx import HTTPError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import Plant
from app.schemas import (
    PlantReadSchemas,
    PlantCreateSchemas,
    PlantUpdatePropSchemas,
)
from jose.jwt import decode
from jose import JWTError, ExpiredSignatureError
from app.config import Config, load_config
from app.logic import (
    createPlant,
    get_all_plant_by_user_id,
    update_plant_property,
    remove_plant_by_id,
)

cfg: Config = load_config()

plant_router = APIRouter(
    prefix="/plants",
    tags=["plants"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_async_session)],
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://127.0.0.1:5000/auth/jwt/login"
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expired_exception = HTTPException(
        status_code=401,
        detail="Token was expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(
            token,
            cfg.SECRET,
            audience="fastapi-users:auth",
            algorithms=["HS256"],
        )
        username: uuid.UUID = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except ExpiredSignatureError:
        raise expired_exception
    except JWTError:
        raise credentials_exception


@plant_router.post("/create", response_model=PlantReadSchemas)
async def create_plant(
    plant: PlantCreateSchemas,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    data = await createPlant(plant=plant, db=db, current_user=current_user)
    return data


@plant_router.get("/", response_model=List[PlantReadSchemas])
async def get_user_plants(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await get_all_plant_by_user_id(db=db, current_user=current_user)


@plant_router.patch(
    "/plant/property/{plant_id}", response_model=PlantUpdatePropSchemas
)
async def change_properties_plant(
    plant_id: uuid.UUID,
    plant: PlantUpdatePropSchemas,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    return await update_plant_property(
        plantID=plant_id, plant=plant, db=db, current_user=current_user
    )


@plant_router.delete("/plant/{plant_id}")
async def remove_plant(
    plant_id: uuid.UUID,
    current_user: Annotated[uuid.UUID, Depends(get_current_user)],
    db: AsyncSession = Depends(get_async_session),
):
    response = await remove_plant_by_id(
        plantID=plant_id, current_user=current_user, db=db
    )
    if response == 0:
        return HTTPException(
            status_code=403, detail="Forbidden: invalid plant_id"
        )
    elif response == 1:
        return HTTPException(status_code=200, detail="Plant was removed")
    return response
