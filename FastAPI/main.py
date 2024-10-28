from fastapi import FastAPI
from routers import products, jwt_auth_users, basic_auth_users, users_db, alumnos
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import redis
import json
from decouple  import config
#
app = FastAPI()

"""origins = [
    "file:///C:/Users/Miguel/Desktop/ReduceMemory/Backend/apis/index.html",
]"""

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



#Api_key = config('API_KEY')

class CityWeather(BaseModel):
    ciudad: str
    paisAbv: str | None = "cl"

rd = redis.Redis(host="localhost", port=6379, db=0)

@app.get("/h")
async def root():
    return {"Hola FastAPI"}

@app.get("/url")
async def root():
    return {"message": "Hola FastAPI"}

@app.post("/weather")
async def read_clima(clima: CityWeather):
    cache = rd.get(clima.ciudad)
    if cache:
        print("cache hit")
        return json.loads(cache)
    else:
        print("cache miss")
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={clima.ciudad},{clima.paisAbv}&APPID=dad390e2ad4a9ec83bf95456eb0f1680") #dejo aqui mi api_key :P
        if r.json()['cod'] == "404":
            f = {"No city found"}
            rd.set(clima.ciudad, "No city found")
            rd.expire(clima.ciudad, 10)
            return f
        else:
            weather = r.json()['weather'][0]['main']
            temp = round(r.json()['main']['temp'])
            f = {"message": f"En {clima.ciudad} el clima es: {weather}, y La temperatura es de: {temp}F"}
            n = json.dumps(f)
            rd.set(clima.ciudad, n)
            rd.expire(clima.ciudad, 10)
            return f

# Solicitud weather pero con path
@app.get("/weather/{ciudad},{pais}")
async def read_clima(ciudad: str, pais: str):
    cache = rd.get(ciudad)
    if cache:
        print("cache hit")
        return json.loads(cache)
    else:
        print("cache miss")
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},{pais}&APPID=dad390e2ad4a9ec83bf95456eb0f1680")
        if r.json()['cod'] == "404":
            f = {"No city found"}
            rd.set(ciudad, "No city found")
            rd.expire(ciudad, 10)
            return f
        else:
            weather = r.json()['weather'][0]['main']
            temp = round(r.json()['main']['temp'])
            f = {"message": f"En {ciudad} el clima es: {weather}, y La temperatura es de: {temp}F"}
            n = json.dumps(f)
            rd.set(ciudad, n)
            rd.expire(ciudad, 10)
            return f