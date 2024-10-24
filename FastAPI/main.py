from fastapi import FastAPI
from routers import products, jwt_auth_users, basic_auth_users, users_db, alumnos
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
#
app = FastAPI()

origins = [
    "file:///C:/Users/Miguel/Desktop/ReduceMemory/Backend/apis/index.html",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers

app.include_router(products.router)
app.include_router(alumnos.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="estático")

@app.get("/h")
async def root():
    return {"Hola FastAPI"}

@app.get("/url")
async def root():
    return {"message": "Hola FastAPI"}