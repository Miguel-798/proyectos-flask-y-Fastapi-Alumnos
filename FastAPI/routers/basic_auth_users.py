from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router=APIRouter(prefix="/basic",
                   tags= ["basic"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

#class form(BaseModel):
#    username: str
#    password: str

users_db = {
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
}


def search_user_DB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# Criterio de dependencia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación invalidas", 
            headers={"WWW-Authenticate": "Bearer"})
    

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_DB(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username , "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

