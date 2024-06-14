
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, JSON
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import relationship

Base: DeclarativeMeta = declarative_base()


class Plant(Base):
    __tablename__ = "plant"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4())
    type = Column(String, nullable=False, default="")
    owner = Column(
        UUID(as_uuid=True),
        nullable=False)
    parther = Column(
        UUID(as_uuid=True),
        nullable=True)
    styles = Column(JSON, nullable=True)
    property = Column(JSON, nullable=True)


# class PlantRequest(Base):
#     __tablename__ = "plant_requests"
#     id = Column(UUID(as_uuid=True), primary_key=True, index=True,
#                 default=uuid4())
#     sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
#                        nullable=False)
#     receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
#                          nullable=False)
#     message = Column(String, nullable=False, default="",)  # pending, accepted, rejected
#     status = Column(String, nullable=False, default="pending")  # pending, accepted, rejected
