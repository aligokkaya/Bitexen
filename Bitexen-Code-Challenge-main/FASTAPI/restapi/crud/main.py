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

@bitexenAPI.get('/v1/bitexen/weekly/{data}')
async def get_week(data:str):
    print(data)
    req=conn.execute(Weekly.select().where(Weekly.c.datetime == str(data))).fetchall()

    responce={
                'min_price':req[0]['min'],
                'max_price':req[0]['max'],
                'avarage_price':req[0]['avarage_price'],
                'total_volume':req[0]['total_volume'],
                'years':str(data)[0:4],
                'month':str(data)[5:7],
                'week':str(data)[8:]

    }
    return responce

@bitexenAPI.get('/v1/bitexen/month/{data}')
async def get_month(data:str):
    req=conn.execute(Monthly.select().where(Monthly.c.datetime == data)).fetchall()
    responce={
                'min_price':req[0]['min'],
                'max_price':req[0]['max'],
                'avarage_price':req[0]['avarage_price'],
                'total_volume':req[0]['total_volume'],
                'years':str(data)[0:4],
                'month':str(data)[5:7]
    }
    return responce



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

