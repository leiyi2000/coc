import os

APP_NAME = "coc"
# 数据库
TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL", default=f"sqlite://{APP_NAME}.sqlite3")},
    "apps": {
        APP_NAME: {
            "models": [f"{APP_NAME}.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "timezone": "Asia/Shanghai",
}
