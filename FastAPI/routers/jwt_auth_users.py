from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
import pymysql.cursors
import pymysql

from fastapi import APIRouter, Depends, HTTPException, status, FastAPI

from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt 
#from jose import JWT, JOSEError
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware



ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 10
SECRET = "fa3f94750744a21e2f5db3ab802020b32b525d26f35929428c14355dd13b3f51"


router=APIRouter()



oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    #disabled: bool

class UserDB(User):
    password: str

"""users_db = {
    "miguel": {
        "username":  "miguel",
        "full_name": "Miguel Alzate",
        "email": "miguelalzate@miguel.com",
        "disabled": False,
        "password": "123456",
    },
    "miguel2": {
        "username":  "miguel2",
        "full_name": "Miguel Alzate 2",
        "email": "alzate.miguel@miguel.com",
        "disabled": False,
        "password": "654321",
    },
    "miguel3": {
        "username":  "miguel3",
        "full_name": "Miguel Alzate 3",
        "email": "miguel.alzate@miguel.com",
        "disabled": False,
        "password": "654321",
    }
}"""

"""def search_user_DB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])"""

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación invalidas", 
            headers={"WWW-Authenticate": "Bearer"})
    
    try:  
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except:
        raise exception
    return get_by_username(username)
        

# Criterio de dependencia
async def current_user(user: User = Depends(auth_user)):

    """if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")"""
    return user



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    #user_db = users_db.get(form.username)
    user_db = get_by_username(form.username)
    if user_db == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    

    user = get_by_usernameDB(form.username)


    #if not crypt.verify(form.password,  user.password):
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user



config = {
    "host": "localhost",
    "port": 3307,
    "database": "academia",
    "user": "root",
    "password": "" 
}

def get_db():
    connection = pymysql.connect(**config)
    return connection

def get_by_username(username):
        db = get_db()
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT username, full_name, email FROM users WHERE username = %s", (username,))
            response = cursor.fetchone()
            if response:
                return User(**response)
            else:
                return None
        
def get_by_usernameDB(username):
    db = get_db()
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT username, full_name, email, password FROM users WHERE username = %s", (username,))
        response = cursor.fetchone()
        if response:
            return UserDB(**response)
        else:
            return None
    
print(get_by_usernameDB("miguel"))