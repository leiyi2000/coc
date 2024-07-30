from fastapi import APIRouter, Body

from coc import models
from coc.constants import NotifyStatus


router = APIRouter()


@router.post("")
async def create(
    timestamp: int = Body(),
    callback: str = Body(),
    payload: dict | None = Body(default=None),
    retry: int = Body(default=0),
):
    return await models.Notify.create(
        timestamp=timestamp,
        callback=callback,
        payload=payload,
        retry=retry,
        status=NotifyStatus.pending,
    )


@router.get("")
async def reads():
    return await models.Notify.all().order_by("-updated_at")
