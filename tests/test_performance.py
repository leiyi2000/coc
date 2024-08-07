import time
import random

import httpx
import pytest


# 定义接口的URL
BASE_URL = "http://10.10.77.52:8020/notify"


# 定义请求函数
def send_request():
    post_data = {
        "timestamp": int(time.time()) + random.randint(1, 10) * 60,
        "callback": "http://10.10.77.52:8030/accept",
        "payload": {},
        "retry": 0,
    }
    response = httpx.post(BASE_URL, json=post_data)
    return response


# 性能测试
@pytest.mark.benchmark(
    group="notify",  # 分组名称
    min_rounds=10,  # 最少运行轮数
    max_time=100,  # 最大运行时间
)
def test_notify_performance(benchmark):
    result = benchmark(send_request)
    assert result.status_code == 200


if __name__ == "__main__":
    pytest.main(["-v", __file__])
