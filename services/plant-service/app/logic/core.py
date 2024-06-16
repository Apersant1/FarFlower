from typing import List
import uuid
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
    current_user: str,
):
    updaing_plant = await db.execute(select(Plant).where(Plant.id == plantID))
    updaing_plant = updaing_plant.scalars().first()
    updaing_plant.property = plant.property
    await db.commit()
    return updaing_plant
