from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, FriendRequest
from app.schemas import FriendRequestSchemaRead, FriendRequestStatus
from sqlalchemy.future import select
from sqlalchemy.sql import text
from sqlalchemy import delete


async def send_request(
    friendID: uuid.UUID, db: AsyncSession, current_user: dict
):
    if not current_user.id:
        return 0
    receiver = await db.execute(select(User).where(User.id == friendID))
    receiver = receiver.scalars().first()
    if not receiver:
        return 2
    existing_request = await db.execute(
        select(FriendRequest).where(
            FriendRequest.sender_id == current_user.id,
            FriendRequest.receiver_id == friendID,
        )
    )
    existing_request = existing_request.scalars().first()
    if existing_request:
        return 3

    new_request = FriendRequest(
        id=uuid.uuid4(),
        sender_id=current_user.id,
        receiver_id=friendID,
        status=FriendRequestStatus.pending,
    )
    db.add(new_request)
    await db.commit()
    return new_request


async def get_request_list(
    userID: uuid.UUID, db: AsyncSession
) -> List[FriendRequestSchemaRead]:

    req_list = await db.execute(
        select(FriendRequest)
        .where(FriendRequest.receiver_id == userID)
        .where(FriendRequest.status == "pending")
    )
    result = req_list.scalars().all()
    return result


async def accept_request(
    requestID: uuid.UUID,
    status: FriendRequestStatus,
    db: AsyncSession,
    current_user: dict,
):
    if current_user is None:
        return 0
    request = await db.execute(
        select(FriendRequest).where(FriendRequest.id == requestID)
    )
    request = request.scalars().first()

    if request is None:
        return 1
    if (
        request.status == FriendRequestStatus.pending
        and status == FriendRequestStatus.accepted
    ):
        request.status = status
        await db.commit()
        return request
    if (
        request.status == FriendRequestStatus.accepted
        and status == FriendRequestStatus.accepted
    ):
        return 2
    if request.status == "accepted" and status == FriendRequestStatus.rejected:
        await db.execute(
            delete(FriendRequest).where(FriendRequest.id == requestID)
        )
        await db.commit()
        return 3


async def get_friends_list(current_user: dict, db: AsyncSession):
    statement_sender = text(
        f"""
        SELECT u.*
        FROM friend_requests fr
        JOIN users u ON fr.receiver_id = u.id
        WHERE fr.sender_id = '{current_user.id}'
        AND fr.status = 'accepted';
    """
    )
    statement_receiver = text(
        f"""
        SELECT u.*
        FROM friend_requests fr
        JOIN users u ON fr.sender_id = u.id
        WHERE fr.receiver_id = '{current_user.id}'
        AND fr.status = 'accepted';
    """
    )
    result_sender = await db.execute(statement_sender)
    result_receiver = await db.execute(statement_receiver)
    friends_sender = result_sender.fetchall()
    friends_receiver = result_receiver.fetchall()
    friends = friends_sender + friends_receiver
    return friends
