import uuid
from typing import List
from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import User
from app.schemas import FriendRequestSchemaRead, FriendRequestStatus, UserRead
from app.query import send_request, get_request_list
from app.query import accept_request, get_friends_list
from app.auth.auth import AuthInitializer
from app.manager import get_user_manager

from app.config import Config, load_config


cfg: Config = load_config()

auth = AuthInitializer()
auth.initializer(cfg.SECRET)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager,
                                              [auth.auth_backend])

current_active_user = fastapi_users.current_user(active=True)


FriendRouter = APIRouter()


@FriendRouter.post("/friends/send-request", tags=['Friend'])
async def send_friend_request(
    friendID: uuid.UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(current_active_user)
):
    answer = await send_request(friendID=friendID,
                                db=db,
                                current_user=current_user)
    if answer == 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    if answer == 2:
        raise HTTPException(status_code=400, detail="Receiver not founds")
    if answer == 3:
        raise HTTPException(status_code=400, detail="Request already exists")
    return answer


@FriendRouter.get("/friend/requests-list", tags=["Friend"],
                  response_model=List[FriendRequestSchemaRead])
async def get_requests_list(
    db: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(current_active_user)
):
    req_list = await get_request_list(userID=current_user.id, db=db)
    return req_list


@FriendRouter.patch("/friend/accept-request", tags=["Friend"])
async def accepting_request(
    requestID: uuid.UUID,
    status: FriendRequestStatus,
    db: AsyncSession = Depends(get_async_session),
    current_user: dict = Depends(current_active_user)
):
    if current_user is None:
        return HTTPException(status_code=401,
                             detail="Authentication required")
    request = await accept_request(requestID=requestID,
                                   status=status,
                                   db=db,
                                   current_user=current_user)
    if request == 0:
        return HTTPException(status_code=403,
                             detail="Forbidden: invalid user")
    elif request == 1:
        return HTTPException(status_code=400,
                             detail="Request not found")
    elif request == 2:
        return HTTPException(status_code=400,
                             detail="Request already accepted")
    elif request == 3:
        return HTTPException(status_code=200,
                             detail="Request was rejected")
    return request


@FriendRouter.get("/friend/friend-list",
                  tags=["Friend"],
                  response_model=List[UserRead])
async def get_friend_list(
    current_user: dict = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session)
):
    return await get_friends_list(current_user=current_user, db=db)
