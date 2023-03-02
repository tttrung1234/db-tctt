from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, validator
from ..database.models import User
from tortoise import Tortoise

Tortoise.init_models(["src.database.models"], "models")

_UserInSchema = pydantic_model_creator(User, name="UserIn", exclude=["id"])
UserOut = pydantic_model_creator(User, name="UserOut")

class Token(BaseModel):
    username: str
    access_token: str
    token_type: str


class UserIn(_UserInSchema):
    @validator('password')
    def check_pwd(cls, v):
        if len(v) < 6:
            raise ValueError('must >= 6 characters')
        
        return v