import mysql.connector
from flask import redirect,url_for,session,request,render_template,make_response,jsonify
from functools import wraps
from app import app
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_restful import Resource, Api
import json
from math import *

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

app.secret_key='super secret key'

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
        
sched = BackgroundScheduler(daemon=True)
sched.add_job(data, 'interval', seconds=5)
sched.start()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for("login"))
    return decorated_function

@app.route("/ucretler",methods=['GET','POST'])
@login_required
def ucretler():
    para=[]
    b_data=[]
    r=requests.get("https://www.bitexen.com/api/v1/market_info/")
    data = json.loads(r.text)
    data=(data['data']['markets'])
    for i in data:
        para.append(i['market_code'])

    if request.method=='POST':
        gelen=request.form.get("para")
        x = requests.get("https://www.bitexen.com/api/v1/ticker/"+str(gelen)+"/")
        data2 = json.loads(x.text)
        dt_object = datetime.fromtimestamp(float(data2['data']['ticker']['timestamp']))
        return render_template("ucretler.html",para=para,data=data2['data']['ticker'],date=dt_object)
    return render_template("ucretler.html",para=para,data=b_data)

@app.route("/raporlar",methods=['GET','POST'])
@login_required
def raporlar():
    if request.method=='POST':

        when=request.form.get("when")
        mydb=db_con()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM "+str(when)+"")
        myresult = mycursor.fetchall()
        return render_template("raporlar.html",myresult=myresult)
    return render_template("raporlar.html")

@app.route('/', methods=["GET", "POST"])
@login_required
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
@login_required
def data():

    x = requests.get('https://www.bitexen.com/api/v1/ticker/')
    data = json.loads(x.text)
    BTCTRY=float(data['data']['ticker']['BTCTRY']['last_price'])
    ETHTRY=float(data['data']['ticker']['ETHTRY']['last_price'])
    data = [(time.time()),(BTCTRY), (ETHTRY)]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get("email")
        password=request.form.get("pass")
        mydb=db_con()
        mycursor = mydb.cursor()
        mycursor.execute("select*from users where mail='"+email+"' and password='"+password+"'")
        myresult=mycursor.fetchall()
        if myresult:
            session["logged_in"]=True
            session["username"]=email
            mycursor.execute("select*from users where mail='"+email+"' ")
            myresult=mycursor.fetchall()
            return render_template("index.html")
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/buysell",methods=['GET','POST'])
@login_required
def buysell():
    
    x = requests.get("https://www.bitexen.com/api/v1/order_book/BTCTRY/")
    data = json.loads(x.text)
    buyers_array =(data['data']['buyers'])
    sellers_array=(data['data']['sellers'])
    transfer=(data['data']['last_transactions'])

    if request.method=='POST':
        buy_sell=request.form.get("buy-sell")
        if buy_sell=='buyers':
            return render_template("buy-sell.html",data=buyers_array)
        elif buy_sell=='sellers':
            return render_template("buy-sell.html",data=sellers_array)
        else :
            return render_template("buy-sell.html",data=transfer)
    return render_template("buy-sell.html")



##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
##############################################################################################################
                                        #########REST_API######################



api = Api(app)

def db_get(data,day):
    if day != 'a':
        mydb=db_con()
        mycursor = mydb.cursor()
        mycursor.execute("select*from "+str(data)+" WHERE datetime = '"+str(day)+"' ")
        # "select*from "+str(data)+" WHERE datetime = '"+str(day)+"' "
        myresult = mycursor.fetchone()
        
        return myresult
    else:
        mydb=db_con()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM "+str(data)+"")
        myresult = mycursor.fetchall()
        return myresult
class Bitexen_Day(Resource):
    def get(self):
        myresult=db_get('daily','a')
        return jsonify({'daily':myresult})

class Bitexen(Resource):
    def get(self,data,day):
        self.data=data
        self.day=day
        if self.data=='daily':
            myresult=db_get(self.data,'a')
            
            return jsonify({str(self.data):myresult})
        elif self.data=='weekly':
            myresult=db_get(self.data,self.day)
            responce={
                'min_price':myresult[1],
                'max_price':myresult[2],
                'avarage_price':myresult[3],
                'total_volume':myresult[4],
                'years':str(day)[0:4],
                'month':str(day)[5:7],
                'week':str(day)[8:]

            }
            return jsonify({str(self.data):responce})
           
        elif self.data=='monthly':
            myresult=db_get(self.data,self.day)
            responce={
                'min_price':myresult[1],
                'max_price':myresult[2],
                'avarage_price':myresult[3],
                'total_volume':myresult[4],
                'years':str(day)[0:4],
                'month':str(day)[5:7]

            }
            return jsonify({str(self.data):responce})
        else:
            print('b')
            return jsonify({'message': 'Wrong Adress /v1/bitexen/'+self.data+'.'})


class Register(Resource):
    def post(self):
        data = request.form.to_dict()
        if len(data['name-surname']) > 1 and len(data['mail']) > 1 and len(data['password']) > 1 :
            mydb=db_con()
            mycursor = mydb.cursor()
            sql = "INSERT INTO users (name_surname,mail, password) VALUES (%s, %s,%s)"
            val = (str(data['name-surname']), str(data['mail']),str(data['password']))
            mycursor.execute(sql, val)
            mydb.commit()
            return make_response(jsonify({'status': 'success'}), 200)
        else :
            return make_response(jsonify({'status': 'username , mail and password cannot be empty'}), 400)

api.add_resource(Bitexen_Day, '/v1/bitexen/daily/')
api.add_resource(Bitexen, '/v1/bitexen/<string:data>/<string:day>/')
api.add_resource(Register, '/challange/register/')

