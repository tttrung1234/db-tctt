from tortoise.contrib.pydantic import pydantic_model_creator
from ..database.models import Target
from datetime import timedelta, timezone, datetime
from tortoise import Tortoise


Tortoise.init_models(["src.database.models"], "models")

TargetIn = pydantic_model_creator(Target, name="TargetIn", exclude=["id", "platform", "mission", "status", "added_time", "disabled_time"])
_TargetOutSchema = pydantic_model_creator(Target, name="TargetOut")


class TargetOut(_TargetOutSchema):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda t: t.astimezone(timezone(timedelta(hours=7))).strftime('%H:%M:%S %d/%m/%Y')
        }