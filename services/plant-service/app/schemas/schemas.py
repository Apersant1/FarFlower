import uuid
from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel


class PlantBaseSchemas(BaseModel):
    class Config:
        from_attributes = True


class PlantCreateSchemas(PlantBaseSchemas):
    type: str
    owner: uuid.UUID
    styles: Optional[dict]
    property: Optional[dict]


class PlantReadSchemas(PlantBaseSchemas):
    id: uuid.UUID
    type: str
    owner: uuid.UUID
    parther: Optional[uuid.UUID]
    styles: Optional[dict]
    property: Optional[dict]