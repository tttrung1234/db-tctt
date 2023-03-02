from tortoise.contrib.pydantic import pydantic_model_creator
from ..database.models import Mission
from tortoise import Tortoise


Tortoise.init_models(["src.database.models"], "models")


MissionIn = pydantic_model_creator(Mission, name="MissionIn", exclude=["id", "targets"])
MissionOut = pydantic_model_creator(Mission, name="MissionOut")