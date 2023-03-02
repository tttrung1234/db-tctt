from fastapi import APIRouter, Depends, status, Body, HTTPException
from ..schemas import platform as platform_schemas
from ..crud import platform as platform_crud
from typing import List
from ..crud.user import getCurrentUser


router = APIRouter(tags=['Platform'], prefix='/platforms')


@router.get('/', response_model=List[platform_schemas.PlatformOut], dependencies=[Depends(getCurrentUser)])
async def getPlatformList():
    try:
        return await platform_crud.getPlatformList()
    except Exception:
        raise HTTPException(status_code=400)
    

@router.post('/new', dependencies=[Depends(getCurrentUser)])
async def addPlatform(platform: platform_schemas.PlatformIn):
    try:
        await platform_crud.addPlatform(platform)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400)