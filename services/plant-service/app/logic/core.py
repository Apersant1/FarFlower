from typing import List
import uuid
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Plant
from app.schemas import (
    PlantCreateSchemas,
    PlantReadSchemas,
    PlantUpdatePropSchemas,
)
from sqlalchemy.future import select
from sqlalchemy.sql import text
from sqlalchemy import delete


async def createPlant(
    plant: PlantCreateSchemas, db: AsyncSession, current_user: str
):
    new_plant = Plant(
        id=uuid.uuid4(),
        type=plant.type,
        owner=current_user,
        styles=plant.styles,
        property=plant.property,
    )
    db.add(new_plant)
    await db.commit()
    return new_plant


async def get_all_plant_by_user_id(db: AsyncSession, current_user: str):
    all_plants = await db.execute(
        select(Plant).where(
            (Plant.owner == current_user) | (Plant.parther == current_user)
        )
    )
    return all_plants.scalars().all()


async def update_plant_property(
    plantID: uuid.UUID,
    plant: PlantUpdatePropSchemas,
    db: AsyncSession,
    current_user: uuid.UUID,
):
    updaing_plant = await db.execute(select(Plant).where(Plant.id == plantID))
    updaing_plant = updaing_plant.scalars().first()
    if updaing_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    if (
        str(updaing_plant.owner) == current_user
        or str(updaing_plant.parther) == current_user
    ):
        updaing_plant.property = plant.property
        await db.commit()
        return updaing_plant
    else:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this plant's property",
        )


async def remove_plant_by_id(
    plantID, db: AsyncSession, current_user: uuid.UUID
):
    data = await db.execute(select(Plant).where(Plant.id == plantID))
    data = data.scalars().first()
    if str(data.owner) == current_user or str(data.parther) == current_user:
        await db.execute(delete(Plant).where(Plant.id == plantID))
        await db.commit()
        return 1
    else:
        return 0
