
from uuid import uuid4
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import relationship

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    cutename = Column(String, nullable=True)
    registered_at = Column(
        TIMESTAMP, default=datetime.now())
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    sent_requests = relationship("FriendRequest",
                                 foreign_keys="FriendRequest.sender_id")
    received_requests = relationship("FriendRequest",
                                     foreign_keys="FriendRequest.receiver_id")


class FriendRequest(Base):
    __tablename__ = "friend_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True,
                default=uuid4())
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
                       nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
                         nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, accepted, rejected
