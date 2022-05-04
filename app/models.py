from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Target(SQLModel, table=True):
    uid: str = Field(..., primary_key=True)
    status_id: int = Field(..., foreign_key="status.id")
    category_id: int = Field(..., foreign_key="category.id")
    group_id: int = Field(..., foreign_key="group.id")
    added_time: Optional[datetime] = None
    disabled_time: Optional[datetime] = None
    active_img: Optional[str] = None
    disabled_img: Optional[str] = None


class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group: str = Field(default=None, primary_key=True)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(default=None, primary_key=True)


class Status(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    status: str