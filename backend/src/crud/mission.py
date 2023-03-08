from ..database import models
from ..schemas import mission as mission_schemas
from tortoise.exceptions import DoesNotExist, IntegrityError
from typing import List


async def addMission(mission: mission_schemas.MissionIn):
    try:
        await models.Mission.create(**mission.dict())
    except IntegrityError as e:
        raise Exception('Conflict')


async def getMissionList() -> mission_schemas.MissionOut:
    try:
        return await mission_schemas.MissionOut.from_queryset(models.Mission.all())
    except DoesNotExist:
        return []
    

async def deleteMission(mission_id: int):
    try:
        mission_obj = await models.Mission.get(id=mission_id)
        await mission_obj.delete()

    except DoesNotExist as e:
        raise Exception('Does not exist')