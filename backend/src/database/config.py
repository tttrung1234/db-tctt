import os
from typing import Optional

from tortoise import Tortoise


# TORTOISE_ORM = {
#     "connections": {"default": os.environ.get("DATABASE_URL")},
#     "apps": {
#         "models": {
#             "models": [
#                 "src.database.models"
#             ],
#             "default_connection": "default"
#         }
#     }
# }

def register_tortoise(
    app,
    config: Optional[dict] = None,
    generate_schemas: bool = False,
) -> None:
    @app.on_event("startup")
    async def init_orm():
        await Tortoise.init(db_url=os.environ.get("DATABASE_URL"), modules={"models": ["src.database.models"]})
        if generate_schemas:
            await Tortoise.generate_schemas()

    @app.on_event("shutdown")
    async def close_orm():
        await Tortoise.close_connections()



# def init_db():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session
