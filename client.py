import requests
import json
import jwt
import time

url = "http://0.0.0.0:5000p/users"

valid_token = jwt.encode({'user_id':'123',"timestamp":int(time.time())}, 
                            'password',
                            algorithm='HS256') 

payload="{\"user_id\":\"123\"}"
headers = {
  'auth': valid_token
}


response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)