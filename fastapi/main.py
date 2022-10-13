from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dependencies import has_access
import user.user
from setting import jwt_config

app = FastAPI()
security = HTTPBasic()


class USER(BaseModel):
    username: str
    password: str

userDetail = {"username": "Arun", "password": "Arun22"}

PROTECTED = [Depends(has_access)]

app.include_router(
    user.user.router,
    prefix="/user",
    dependencies=PROTECTED
)

@app.get("/")
def root():
    return {"message": "Welcome, This is Unauthorized API"}

@app.post("/login", status_code=200)
def login(loginUser: USER):
    message = ''
    if loginUser.username != userDetail.get("username"):
        message = 'User not found'
        raise HTTPException(status_code=400,detail=message)
    elif loginUser.password != userDetail.get("password"):
        message = 'Password mismatch'
        raise HTTPException(status_code=400,detail=message)
    else:
        expires_time = datetime.utcnow() + timedelta(minutes=jwt_config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        token = jwt.encode({'id':loginUser.username,'exp': expires_time},jwt_config.get("SECRET_KEY"), algorithm=jwt_config.get("ALGORITHM"))
        message = 'Login successfully'
    return{ 'result': {'message': message, 'token': token}}
