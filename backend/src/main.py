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