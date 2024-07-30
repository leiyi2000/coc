from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "notify" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "timestamp" INT NOT NULL  /* 触发时间戳精度秒 */,
    "callback" VARCHAR(255) NOT NULL  /* 回调地址 */,
    "payload" JSON   /* 回调负载内容 */,
    "retry" INT NOT NULL  /* 回调失败后最大重试次数 */,
    "status" VARCHAR(32) NOT NULL  /* 状态 */,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_notify_status_9b7c05" ON "notify" ("status");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
