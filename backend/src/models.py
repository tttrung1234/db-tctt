from sqlmodel import SQLModel, Field, Relationship, Column, Integer, ForeignKey, String
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from pydantic import validator, HttpUrl


class Credential(SQLModel):
    username: str
    password: str


class User(Credential, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class Token(SQLModel):
    username: str
    access_token: str
    token_type: str
    

class Mission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mission_name: str = Field(...)

    targets: List["Target"] = Relationship(back_populates="mission", 
                                            sa_relationship_kwargs={"cascade": "all,delete"})


class Platform(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    platform_name: str = Field(...)

    targets: List["Target"] = Relationship(back_populates="platform", 
                                            sa_relationship_kwargs={"cascade": "all,delete"})


class TargetEdit(SQLModel):
    url: HttpUrl
    platform_id: int
    mission_id: Optional[int]
    active_img: Optional[str] = None
    disabled_img: Optional[str] = None


class Target(SQLModel, table=True):
    url: str = Field(..., primary_key=True)
    platform_id: int = Field(sa_column=Column(Integer, ForeignKey("platform.id", ondelete="CASCADE")))
    mission_id: int = Field(sa_column=Column(Integer, ForeignKey("mission.id", ondelete="CASCADE")))
    status: Optional[bool] = True
    added_time: Optional[datetime] = None
    disabled_time: Optional[datetime] = None
    active_img: Optional[str] = None
    disabled_img: Optional[str] = None

    platform: Platform = Relationship(back_populates="targets")
    mission: Mission = Relationship(back_populates="targets")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda t: t.astimezone(timezone(timedelta(hours=7))).strftime('%H:%M:%S %d/%m/%Y')
        }
