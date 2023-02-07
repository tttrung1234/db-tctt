from fastapi import FastAPI, Depends, status, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .db import get_session, init_db
from . import crud
from . import models
from .auth import getCurrentUser, ACCESS_TOKEN_LIFESPAN, authenticateUser, createAccessToken
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List, Optional, Union
from datetime import timedelta

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    init_db()


@app.post("/signin", response_model=models.Token, status_code=status.HTTP_200_OK)
def signIn(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
# def signIn(form_data: models.Credential, session: Session = Depends(get_session)):

    try:
        current_user = authenticateUser(session, username=form_data.username, password=form_data.password)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_LIFESPAN)
    access_token = createAccessToken(data={'sub': current_user.username}, 
                                            expires_delta=access_token_expires)

    return {"username": current_user.username, "access_token": access_token, "token_type": "bearer"}



@app.post("/signup", response_model=models.Token, status_code=status.HTTP_201_CREATED)
def signUp(account: models.Credential, session: Session = Depends(get_session)):
    # kiểm tra xem username đã tồn tại trên DB chưa
    try:
        user = crud.getUser(session=session, username=account.username)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already registered")

    try:
        new_user = crud.createUser(session, account)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Create new user failed")

    print(new_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_LIFESPAN)
    access_token = createAccessToken(data={'sub': new_user.username}, 
                                        expires_delta=access_token_expires)

    return {"username": new_user.username, "access_token": access_token, "token_type": "Bearer"}


@app.get('/targets', response_model=List[models.Target], 
                    dependencies=[Depends(getCurrentUser)],
                    description="get targets")
def getTargets(session: Session = Depends(get_session)):
    try:
        return crud.getTargets(session, status)
    except Exception as e:
        raise HTTPException(status_code=403)


@app.post('/targets/new', dependencies=[Depends(getCurrentUser)],
                            description="add targets")
def addTargets(target_list: List[models.TargetEdit],
                session: Session = Depends(get_session)):
    try:
        crud.addTargets(session, target_list)
    except Exception as e:
        raise HTTPException(status_code=403)


@app.post('/missions/new', dependencies=[Depends(getCurrentUser)],
                            description="create new mission")
def addMission(mission_name: str = Body(..., embed=True),
            session: Session = Depends(get_session)):
    try:
        crud.addMission(session, mission_name)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403)


@app.delete('/missions/{mission_id}', dependencies=[Depends(getCurrentUser)],
                                    description="delete mission")
def deleteMission(mission_id: int,
                session: Session = Depends(get_session)):
    try:
        return crud.deleteMission(session, mission_id)
    except Exception as e:
        raise HTTPException(status_code=403)


@app.post('/platforms/new', dependencies=[Depends(getCurrentUser)], 
                            description="create new platform")
def addPlatform(platform_name: str = Body(..., embed=True),
            session: Session = Depends(get_session)):
    try:
        crud.addPlatform(session, platform_name)
    except Exception as e:
        print(e)

        raise HTTPException(status_code=403)