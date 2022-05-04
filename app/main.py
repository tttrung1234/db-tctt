from fastapi import Depends, FastAPI, status, Body, HTTPException

from app.db import get_session, init_db
import app.crud as crud
from app.models import Target, Category, Group
from typing import List
from sqlmodel import Session

app = FastAPI(root_path='/api')


@app.on_event("startup")
async def on_startup():
    init_db()


@app.get("/ping", status_code=status.HTTP_200_OK)
def pong():
    return "pong"



@app.get('/targets', status_code=status.HTTP_200_OK, response_model=List[Target] ,description="add targets")
def getTargets(status: int,
                session: Session = Depends(get_session)):
    try:
        return crud.getTargets(status, session)
    except Exception as e:
        raise HTTPException(status_code=403)


@app.post('/targets', status_code=status.HTTP_200_OK, description="add targets")
def addTargets(target_list: List[Target],
                session: Session = Depends(get_session)):
    try:
        crud.addTargets(target_list, session)
    except Exception as e:
        raise HTTPException(status_code=403)


@app.post('/group', status_code=status.HTTP_200_OK, description="create new group")
def addGroup(group_name: str = Body(..., embed=True),
            session: Session = Depends(get_session)):
    try:
        crud.addGroup(group_name, session)
    except Exception as e:
        raise HTTPException(status_code=403)


@app.post('/category', status_code=status.HTTP_200_OK, description="create new category")
def addCategory(cat_name: str = Body(..., embed=True),
            session: Session = Depends(get_session)):
    try:
        crud.addCategory(cat_name, session)
    except Exception as e:
        raise HTTPException(status_code=403)