from ..database import models
from ..schemas import platform as platform_schemas
from tortoise.exceptions import DoesNotExist, IntegrityError
from typing import List


async def addPlatform(platform: platform_schemas.PlatformIn):
    try:
        await models.Platform.create(**platform.dict())
    except IntegrityError as e:
        raise Exception('Conflict')


async def getPlatformList() -> List[platform_schemas.PlatformOut]:
    try:
        return await platform_schemas.PlatformOut.from_queryset(models.Platform.all())
    except DoesNotExist:
        return []
    

async def deletePlatform(platform_id: int):
    try:
        platfrom_obj = await models.Platform.get(id=platform_id)
        await platfrom_obj.delete()

    except DoesNotExist as e:
        raise Exception('Does not exist')