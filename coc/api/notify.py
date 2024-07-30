from fastapi import APIRouter, Body

from coc import models, timer
from coc.constants import NotifyStatus


router = APIRouter()


@router.post("")
async def create(
    timestamp: int = Body(),
    callback: str = Body(),
    payload: dict | None = Body(default=None),
    retry: int = Body(default=0),
):
    notify = await models.Notify.create(
        timestamp=timestamp,
        callback=callback,
        payload=payload,
        retry=retry,
        status=NotifyStatus.pending,
    )
    job = timer.Job(notify.id, callback, payload, timestamp, retry)
    timer.Timer.push(job)
    return notify


@router.get("")
async def reads():
    return await models.Notify.all().order_by("-updated_at")
