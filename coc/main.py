import asyncio
from contextlib import asynccontextmanager

from aerich import Command
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from coc.api import router
from coc import models, timer
from coc.constants import NotifyStatus
from coc.settings import APP_NAME, TORTOISE_ORM


async def reload_timer():
    """重新加载定时器

    1. 分库防止重复注册
    """
    async for notify in models.Notify.filter(status=NotifyStatus.pending):
        job = timer.Job(
            notify.id,
            notify.callback,
            notify.payload,
            notify.timestamp,
            notify.retry,
        )
        timer.Timer.push(job)


@asynccontextmanager
async def lifespan(app: FastAPI):
    command = Command(
        tortoise_config=TORTOISE_ORM,
        app=APP_NAME,
        location="./migrations",
    )
    await command.init()
    await command.upgrade(run_in_transaction=True)
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        add_exception_handlers=False,
    )
    await reload_timer()
    # 定时器开始轮询
    asyncio.create_task(timer.Timer.run())
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
