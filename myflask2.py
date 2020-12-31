from flask import Flask
from flask_restful import Api
from user_controller import Users     #引用自創類別，假裝是輸入方的指令

app = Flask(__name__)
api = Api(app)                  #做一個api變數，引用python flask_restful中的套件 Api 函式


api.add_resource(Users , "/users")    # 為我們api也就是app變數，新增指令
                                      #這段程式碼在說，當我到了https://....../user會執行User這個類別

@app.route('/') 

def index():
    return "Hello World"

if __name__ == "__main__":    
    app.debug = True          
    app.run(host = '127.0.0.1',port = 5000)  