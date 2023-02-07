from . import models
from datetime import datetime, timedelta
from sqlmodel import Session, select, func
from typing import List, Optional
from .auth import hashPassword
import json


def exception_handler(fn):
    def wrapprer(*args, **kargs):
        try:
            return fn(*args, **kargs)
        except Exception as e:
            print(f'Error: {e}')
            print(f'At: {fn.__name__}')

    return wrapprer


@exception_handler
def getUser(session: Session, username: str) -> models.User:
    statement = select(models.User).where(models.User.username == username)
    return session.exec(statement).first()


@exception_handler
def createUser(session: Session, cred: models.Credential) -> models.User:
    password = hashPassword(cred.password)

    new_user = models.User(username=cred.username, password=password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@exception_handler
def addTargets(session: Session, target_list: List[models.TargetEdit]):
    now = datetime.now()

    for item in target_list:
        target = models.Target(**item.dict(), added_time=now)
        session.add(target)
    
    session.commit()


@exception_handler
def getTargets(session: Session, status: int):
    return session.exec(select(models.Target)).all()



@exception_handler
def addPlatform(session: Session, platform_name: str):
    new_platform = models.Platform(platform_name=platform_name)
    session.add(new_platform)
    session.commit()


@exception_handler
def addMission(session: Session, mission_name: str):
    new_mission = models.Mission(mission_name=mission_name)
    session.add(new_mission)
    session.commit()


@exception_handler
def deleteMission(session: Session, mission_id: int):
    statement = select(models.Mission).where(models.Mission.id == mission_id)
    mission = session.exec(statement).one()
    
    session.delete(mission)
    session.commit()