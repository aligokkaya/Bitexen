import requests
from math import *
import mysql.connector
import time
import json
from datetime import datetime

db_save=[]
daily=[]
min_week,max_week,average_week,total_volume_week,last_price_week=0.0,0.0,0.0,0.0,0.0
min_monthly,max_monthly,average_monthly,total_volume_monthly,last_price_monthly=0.0,0.0,0.0,0.0,0.0
buyers_array=[]
sellers_array=[]
sayac=0

def db_con():
    mydb = mysql.connector.connect(
    host="hypegenai.com",
    user="hypegena",
    password="aZ5xjXf133",
    database="hypegena_b_challenge")

    return mydb


def data():
    global min_week,max_week,average_week,total_volume_week,last_price_week
    global min_monthly,max_monthly,average_monthly,total_volume_monthly,last_price_monthly
    global sayac
    time.sleep(1)
    try:
        x = requests.get("https://www.bitexen.com/api/v1/order_book/BTCTRY/")
        data = json.loads(x.text)
        min = float(data['data']['ticker']['low_24h'])
        max = float(data['data']['ticker']['high_24h'])
        last_price = float(data['data']['ticker']['last_price'])
        daily_avarage_price= float(data['data']['ticker']['avg_24h'])
        volume_24h=float(data['data']['ticker']['volume_24h'])
        timestamp=datetime.fromtimestamp(float(data['data']['ticker']['timestamp']))

        new_data={

            'min':min,
            'max':max,
            'daily_avarage_price':daily_avarage_price,
            'volume_24h':volume_24h,
            'last_price':last_price
        }
        db_save.append(new_data)
        if len(db_save) >=2:
            if db_save[0] != db_save[1]:
                mydb=db_con()
                mycursor = mydb.cursor()
                sql = "INSERT INTO statistic_points (min, max,average,total_volume,last_price,datetime) VALUES (%s, %s,%s, %s,%s, %s)"
                val = (str(db_save[1]['min']), str(db_save[1]['max']),str(db_save[1]['daily_avarage_price']),str(db_save[1]['volume_24h']),str(db_save[1]['last_price']),str(timestamp))
                mycursor.execute(sql, val)
                mydb.commit()
            del db_save[0]
        d_total=(str(datetime.now())[11:16])
        if d_total == '00:00':
            if sayac==0:
                sayac+=1
                mydb=db_con()
                mycursor = mydb.cursor()
                sql = "INSERT INTO daily (min, max,avarage_price,total_volume,last_price,datetime) VALUES (%s, %s,%s, %s,%s, %s)"
                val = (str(db_save[0]['min']), str(db_save[0]['max']),str(db_save[0]['daily_avarage_price']),str(db_save[0]['volume_24h']),str(db_save[0]['last_price']),str(timestamp))
                mycursor.execute(sql, val)
                mydb.commit()
                daily.append(db_save[0])

        # print(timestamp)
        years_month=str(timestamp)[0:7]
        week=str(timestamp)[9:11]
        week=floor(int(week)/7)
 
        if len(daily) % 7 == 0 and len(daily) > 0:
            for i in range(len(daily)):
                min_week=(min_week+daily[i]['min'])
                max_week=(max_week+daily[i]['max'])
                average_week=(average_week+daily[i]['daily_avarage_price'])       
                total_volume_week=(total_volume_week+daily[i]['volume_24h']) 
                last_price_week=(last_price_week+daily[i]['last_price'])

            
            mydb=db_con()
            mycursor = mydb.cursor()
            sql = "INSERT INTO weekly (min, max,avarage_price,total_volume,last_price,datetime) VALUES (%s, %s,%s, %s,%s, %s)"
            val = ((float(min_week/len(daily))) , (float(max_week/len(daily))),(float(average_week/len(daily))),(float(total_volume_week/len(daily))),(float(last_price_week/len(daily))),(str(years_month)+""+str(week)))
            mycursor.execute(sql, val)
            mydb.commit()
            min_week,max_week,average_week,total_volume_week,last_price_week=0.0,0.0,0.0,0.0,0.0
 
        if len(daily) % 30==0 and len(daily) > 0:
            for i in range(len(daily)):
                min_monthly=min_monthly+daily[i]['min']
                max_monthly=max_monthly+daily[i]['max']
                average_monthly=average_monthly+daily[i]['daily_avarage_price']
                total_volume_monthly=total_volume_monthly+daily[i]['volume_24h']
                last_price_monthly=last_price_monthly+daily[i]['last_price']

            mydb=db_con()
            mycursor = mydb.cursor()
            sql = "INSERT INTO monthly (min, max,avarage_price,total_volume,last_price,datetime) VALUES (%s, %s,%s, %s,%s, %s)"
            val = ((float(min_monthly/len(daily))) , (float(max_monthly/len(daily))),(float(average_monthly/len(daily))),(float(total_volume_monthly/len(daily))),(float(last_price_monthly/len(daily))),(str(years_month)))
            mycursor.execute(sql, val)
            mydb.commit()
            min_monthly,max_monthly,average_monthly,total_volume_monthly,last_price_monthly=0.0,0.0,0.0,0.0,0.0
    except Exception as inst:
       print(inst)

while True:
    time.sleep(5)
    print('burdayim')
    data()