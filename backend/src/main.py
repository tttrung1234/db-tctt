import mailcap
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.config import register_tortoise
from tortoise import Tortoise
from .routes import target, user, platform, mission

Tortoise.init_models(["src.database.models"], "models")

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

app.include_router(user.router)
app.include_router(target.router)
app.include_router(platform.router)
app.include_router(mission.router)

register_tortoise(app, generate_schemas=True)






# @app.post('/missions/new', dependencies=[Depends(getCurrentUser)],
#                             description="create new mission")
# def addMission(mission_name: str = Body(..., embed=True),
#             session: Session = Depends(get_session)):
#     try:
#         crud.addMission(session, mission_name)
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=403)


# @app.delete('/missions/{mission_id}', dependencies=[Depends(getCurrentUser)],
#                                     description="delete mission")
# def deleteMission(mission_id: int,
#                 session: Session = Depends(get_session)):
#     try:
#         return crud.deleteMission(session, mission_id)
#     except Exception as e:
#         raise HTTPException(status_code=403)


# @app.post('/platforms/new', dependencies=[Depends(getCurrentUser)], 
#                             description="create new platform")
# def addPlatform(platform_name: str = Body(..., embed=True),
#             session: Session = Depends(get_session)):
#     try:
#         crud.addPlatform(session, platform_name)
#     except Exception as e:
#         print(e)

#         raise HTTPException(status_code=403)