from fastapi import APIRouter


router = APIRouter()


@router.get("/health", description="健康检查", tags=["探针"])
async def health():
    return True
