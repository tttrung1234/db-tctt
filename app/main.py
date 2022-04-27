from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session, init_db
from app.models import Song, SongCreate

from typing import List
from datetime import datetime

app = FastAPI(root_path='/api/v1')


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/ping")
async def pong():
    return {"pong": datetime.now()}


@app.get("/songs", response_model=List[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, id=song.id) for song in songs]


@app.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song