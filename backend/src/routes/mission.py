from fastapi import APIRouter, Depends, status, Body, HTTPException
from ..schemas import mission as mission_schemas
from ..crud import mission as mission_crud
from typing import List
from ..crud.user import getCurrentUser


router = APIRouter(tags=['Mission'], prefix='/missions')


@router.get('/', response_model=List[mission_schemas.MissionOut], dependencies=[Depends(getCurrentUser)])
async def getMissionList():
    try:
        return await mission_crud.getMissionList()
    except Exception:
        raise HTTPException(status_code=400)
    

@router.post('/new', description="add mission", dependencies=[Depends(getCurrentUser)])
async def addMission(mission: mission_schemas.MissionIn):
    try:
        await mission_crud.addMission(mission)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)
    

@router.delete('/{mission_id}', dependencies=[Depends(getCurrentUser)])
async def deleteMission(mission_id: int):
    try:
        await mission_crud.deleteMission(mission_id)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)