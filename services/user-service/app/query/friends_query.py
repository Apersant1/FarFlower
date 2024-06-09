from typing import List
import uuid
from fastapi import APIRouter,Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import User, FriendRequest
from app.schemas import FriendRequestSchemaRead, FriendRequestSchemaCreate, FriendRequestBase
from sqlalchemy.future import select


async def send_request(req: FriendRequestSchemaCreate,
                       db: AsyncSession):
    sender = await db.execute(select(User).where(User.id == req.sender_id))
    sender = sender.scalars().first()
    if not sender:
        return 1
    receiver = await db.execute(select(User).where(User.id == req.receiver_id))
    receiver = receiver.scalars().first()
    if not receiver:
        return 2
    existing_request = await db.execute(select(FriendRequest)
                                         .where(FriendRequest.sender_id == req.sender_id,
                                                FriendRequest.receiver_id == req.receiver_id))
    existing_request = existing_request.scalars().first()
    if existing_request:
        return 3
    
    new_request = FriendRequest(id=uuid.uuid4(),
                                sender_id=req.sender_id,
                                receiver_id=req.receiver_id,
                                status=req.status)
    db.add(new_request)
    await db.commit()
    return new_request

async def get_request_list(userID: uuid.UUID, db: AsyncSession) -> List[FriendRequestSchemaRead]:
    req_list = await db.execute(select(FriendRequest).where(FriendRequest.receiver_id == userID))
    result = req_list.scalars().all()
    return result