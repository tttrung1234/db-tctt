from tortoise.contrib.pydantic import pydantic_model_creator
from ..database.models import Platform
from tortoise import Tortoise


Tortoise.init_models(["src.database.models"], "models")


PlatformIn = pydantic_model_creator(Platform, name="PlatformIn", exclude=["id", "targets"])
PlatformOut = pydantic_model_creator(Platform, name="PlatformOut")