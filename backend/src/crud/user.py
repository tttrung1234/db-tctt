from ..database import models
from ..schemas import user as user_schemas
from ..auth import jwthandler as auth
from tortoise.exceptions import DoesNotExist, IntegrityError
from fastapi.exceptions import HTTPException
from fastapi import status, Depends


async def getUser(username: str) -> user_schemas.UserOut:
    try:
        return await user_schemas.UserOut.from_queryset_single(models.User.get(username=username))
    except DoesNotExist:
        return None
    

async def createUser(cred: user_schemas.UserIn) -> user_schemas.UserOut:
    password = auth.hashPassword(cred.password)
    try:
        return await models.User.create(username=cred.username, password=password)
    except IntegrityError as e:
        print(e)
        raise auth.AuthError('username already existed')


async def getCurrentUser(token: str = Depends(auth.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = auth.checkToken(token)

    user = await getUser(username=username)
    
    if not user:
        raise credentials_exception

    return user


async def authenticateUser(*, username: str, password: str):
    user = await getUser(username)
    
    if not user:
        raise auth.AuthError('Invalid username or password')
    
    if not auth.verifyPassword(password, user.password):
        raise auth.AuthError('Invalid username or password')

    return user


# @exception_handler
# def addPlatform(session: Session, platform_name: str):
#     new_platform = models.Platform(platform_name=platform_name)
#     session.add(new_platform)
#     session.commit()


# @exception_handler
# def addMission(session: Session, mission_name: str):
#     new_mission = models.Mission(mission_name=mission_name)
#     session.add(new_mission)
#     session.commit()


# @exception_handler
# def deleteMission(session: Session, mission_id: int):
#     statement = select(models.Mission).where(models.Mission.id == mission_id)
#     mission = session.exec(statement).one()
    
#     session.delete(mission)
#     session.commit()