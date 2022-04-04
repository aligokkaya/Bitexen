import requests

r=requests.get('http://127.0.0.1:8000/v1/bitexen/week/2022-04-02/')

print(r.text)