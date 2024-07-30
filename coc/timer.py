from typing import List

import time
import heapq
import asyncio
import traceback
from uuid import UUID

import httpx
import structlog

from coc import models
from coc.constants import NotifyStatus


log = structlog.get_logger()


class Job:
    def __init__(
        self,
        id: str | UUID,
        callback: str,
        payload: dict | None,
        trigger_timestamp: int,
        retry: int,
    ) -> None:
        """Job.

        Args:
            id (str | UUID): 通知任务ID.
            callback (str): 通知接口地址.
            payload (dict | None): 回传数据.
            trigger_timestamp (int): 触发函数执行的时间戳单位秒.
            retry (int): 重试次数.
        """
        self.id = id
        self.callback = callback
        self.payload = payload
        self.trigger_timestamp = trigger_timestamp
        self.retry = retry

    async def _run(self):
        async with httpx.AsyncClient() as client:
            post_data = {
                "id": str(self.id),
                "payload": self.payload,
            }
            response = await client.post(self.callback, json=post_data)
            response.raise_for_status()

    async def run(self):
        error = None
        error_message = None
        for _ in range(max(self.retry, 1)):
            try:
                await self._run()
                await models.Notify.filter(id=self.id).update(
                    status=NotifyStatus.complete
                )
                return
            except Exception as e:
                error = e
                error_message = traceback.format_exc()
        await models.Notify.filter(id=self.id).update(status=NotifyStatus.exception)
        log.exception(error_message)
        raise error

    def __lt__(self, other: "Job"):
        return self.trigger_timestamp < other.trigger_timestamp


class _Timer:
    def __init__(
        self,
        interval: int,
    ) -> None:
        """定时器.

        Args:
            interval (int): 轮询间隔单位秒.
        """
        self.interval = interval
        self.heap: List[Job] = []

    def push(self, job: Job):
        heapq.heappush(self.heap, job)

    async def run(self):
        while True:
            while self.heap and self.heap[0].trigger_timestamp <= int(time.time()):
                job = heapq.heappop(self.heap)
                asyncio.create_task(job.run())
            await asyncio.sleep(self.interval)


Timer = _Timer(interval=1)
