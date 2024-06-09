import uuid
from typing import List
from fastapi import APIRouter,Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import User, FriendRequest
from app.schemas import FriendRequestSchemaCreate, FriendRequestSchemaRead,FriendRequestStatus
from app.query import send_request, get_request_list,accept_request


FriendRouter = APIRouter()


@FriendRouter.post("/friends/send-request", tags=['Friend'])
async def send_friend_request(req: FriendRequestSchemaCreate,
                              db: AsyncSession = Depends(get_async_session)):
    answer = await send_request(req=req, db=db)
    if answer == 1:
        return HTTPException(status_code=400, detail="Sender not founds")
    elif answer == 2:
        return HTTPException(status_code=400, detail="Receiver not founds")
    elif answer == 3:
        return HTTPException(status_code=400, detail="Request already exists")
    return answer

@FriendRouter.get("/friend/requests-list", tags=["Friend"], response_model=List[FriendRequestSchemaRead])
async def get_requests_list(userID: uuid.UUID,
                            db: AsyncSession = Depends(get_async_session)):
    req_list = await get_request_list(userID=userID, db=db)
    return req_list


@FriendRouter.patch("/friend/accept-request", tags=["Friend"])
async def accepting_request(requestID: uuid.UUID,
                         status: FriendRequestStatus,
                         db: AsyncSession = Depends(get_async_session)):
    answer = await accept_request(requestID=requestID, status=status, db=db)
    if answer == 1:
        return HTTPException(status_code=400, detail="Request not found")
    elif answer == 2:
        return HTTPException(status_code=400, detail="Request already accepted")

    return answer
