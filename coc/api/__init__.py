from fastapi import APIRouter

from coc.api import notify

router = APIRouter()


@router.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True


router.include_router(
    notify.router,
    prefix="/notify",
    tags=["定时通知"],
)
