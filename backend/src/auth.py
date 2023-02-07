from typing import Optional
from sqlmodel import Session

from passlib.context import CryptContext
from jose import JWTError, jwt

from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta

from . import crud
from .db import get_session


SECRET_KEY = "daf408fa4b18d7064c39271dcb86ef86d2b4162fb29598d8085485dbc5eddc52"
ALGORITHM = "HS256"
ACCESS_TOKEN_LIFESPAN = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class AuthError(Exception):
    pass


def verifyPassword(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)


def hashPassword(plain_pwd):
    return pwd_context.hash(plain_pwd)


def authenticateUser(session: Session, *, username: str, password: str):
    user = crud.getUser(session, username)

    if not user:
        raise AuthError('Invalid username or password')
    if not verifyPassword(password, user.password):
        raise AuthError('Invalid username or password')

    return user


def createAccessToken(data, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def checkToken(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        
    except JWTError as e:
        print(f'Lỗi: {e}')
        raise credentials_exception

    return username


def getCurrentUser(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = checkToken(token)

    user = crud.getUser(session, username=username)

    if user is None:
        raise credentials_exception

    return user