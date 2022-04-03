
import requests
import cv2 
import json


headers = {'Accept': 'application/json', }
data = {
        'name_surname': 'ali123',
        'mail' :  'ali1@gmail.com',
        'password':'test1234'
        }


res = requests.post("http://0.0.0.0:5000/v1/bitexen/users/",data=json.dumps(data),headers=headers)

print((res.text))
