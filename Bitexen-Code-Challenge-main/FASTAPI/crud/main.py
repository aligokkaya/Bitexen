from fastapi import APIRouter,FastAPI
import requests
from database.database import conn
from fastapi.responses import JSONResponse
from schemas.daily import Daily
from schemas.week import Weekly
from schemas.month import Monthly
from schemas.users import Users
from models.users import User


app = FastAPI()
bitexenAPI = APIRouter()


@bitexenAPI.get('/v1/bitexen/BTCTRY/')
async def btctry():

    r=requests.get('https://www.bitexen.com/api/v1/ticker/BTCTRY/')
    r=r.text
    return JSONResponse(r)

@bitexenAPI.get('/v1/bitexen/daily/')
async def get_daily():
    return conn.execute(Daily.select()).fetchall()

@bitexenAPI.get('/v1/bitexen/week/')
async def get_week():
    return conn.execute(Weekly.select()).fetchall()

@bitexenAPI.get('/v1/bitexen/month/')
async def get_month():
    return conn.execute(Monthly.select()).fetchall()



@bitexenAPI.post('/v1/bitexen/users/')
async def user_save(save:User):
    #conn.execute(companyData.insert().values(companyDatas.companyName))
    print(type(save))
    conn.execute(Users.insert().values(
        mail = save.mail,
        name_surname = save.name_surname,
        password = save.password 
    ))
    return JSONResponse({'status':'ok'}),200

