from flask import Flask
from flask_restful import Api
from user_controller import Users

app = Flask(__name__)   #將我們的api serve裝進我們的變數中
api = Api(app)


api.add_resource(Users , "/users")

@app.route('/')        #@app就是將app變數丟給Flask函式，呼叫路由，'/'代表首頁
def index():
    return "Hello World"

if __name__ == "__main__":    #是不是用的是py3的主程式
    app.debug = True          #開起偵錯模式
    app.run(host = '127.0.0.1',port = 5000)   #程式跑起來阿~~~