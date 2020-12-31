from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
from requests import request
from pprint import pprint

app_id = 'YOUR APP ID(L1)'
app_key = 'YOUR APP KEY(L1)'

class Auth():
    
    def __init__(self, app_id, app_key):                 #建構器
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))    #datetime.now().timetuple()將目前時間轉換
                                                                        #time.struct_time(tm_year=2020, tm_mon=12, 
                                                                        #tm_mday=31, tm_hour=21, tm_min=6, tm_sec=10,
                                                                        #tm_wday=3, tm_yday=366, tm_isdst=-1)
                                                                        #它接收struct_time對像作為參數，返回用秒數來表示時間的浮點數
                                                                        
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)   #一個金鑰和一個訊息作為輸入，生成一個訊息摘要作為輸出
        signature = base64.b64encode(hashed.digest()).decode()                                      #基於給定密鑰key和digest返回msg的摘要

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == '__main__':
    a = Auth(app_id, app_key)
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei?$top=30&$format=JSON', headers= a.get_auth_header())
    pprint(response.content)