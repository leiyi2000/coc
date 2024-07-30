from tortoise import models, fields


class Notify(models.Model):
    id = fields.UUIDField(pk=True)
    timestamp = fields.IntField(description="触发时间戳精度秒")
    callback = fields.CharField(max_length=255, description="回调地址")
    payload = fields.JSONField(null=True, description="回调负载内容")
    retry = fields.IntField(description="回调失败后最大重试次数")
    status = fields.CharField(max_length=32, index=True, description="状态")

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
