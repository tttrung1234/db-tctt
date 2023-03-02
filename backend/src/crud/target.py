from ..database import models
from ..schemas import target as target_schemas
from tortoise.exceptions import DoesNotExist, IntegrityError
from typing import List


async def addTargets(target_list: List[target_schemas.TargetIn]):
    for item in target_list:
        try:
            await models.Target.create(**item.dict())
        except IntegrityError as e:
            raise Exception('Conflict')


async def getTargetList():
    try:
        return await target_schemas.TargetOut.from_queryset(models.Target.all())
    except DoesNotExist:
        return []