from fastapi import APIRouter, Depends, status, Body, HTTPException
from ..schemas import target as target_schemas
from ..crud import target as target_crud
from typing import List
from ..crud.user import getCurrentUser


router = APIRouter(tags=["Target"], prefix='/targets')


@router.get('/', response_model=List[target_schemas.TargetOut], dependencies=[Depends(getCurrentUser)])
async def getTargetList():
    try:
        return await target_crud.getTargetList()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)


@router.post('/new', description="add targets", dependencies=[Depends(getCurrentUser)])
async def addTargets(target_list: List[target_schemas.TargetIn]):
    try:
        await target_crud.addTargets(target_list)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403)