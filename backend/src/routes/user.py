from fastapi import APIRouter, Depends, status, Body, HTTPException
from ..schemas import user as user_schemas
from ..crud import user as user_crud
from ..auth.jwthandler import ACCESS_TOKEN_LIFESPAN, createAccessToken
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


router = APIRouter(tags=['User'])

@router.post("/signin", status_code=status.HTTP_200_OK, response_model=user_schemas.Token)
async def signIn(form_data: OAuth2PasswordRequestForm = Depends()):

    try:
        current_user = await user_crud.authenticateUser(username=form_data.username, password=form_data.password)
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



@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=user_schemas.Token)
async def signUp(account: user_schemas.UserIn):
    # kiểm tra xem username đã tồn tại trên DB chưa
    try:
        user = await user_crud.getUser(username=account.username)
    except Exception:
        raise HTTPException(status_code=401)
    
    if not user:
        try:
            new_user = await user_crud.createUser(account)
        except Exception:
            raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_LIFESPAN)
        access_token = createAccessToken(data={'sub': new_user.username}, 
                                        expires_delta=access_token_expires)
        print(new_user)
        return {"username": new_user.username, "access_token": access_token, "token_type": "Bearer"}

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already registered")