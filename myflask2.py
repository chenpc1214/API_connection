from flask import Flask
from flask_restful import Api
from users_controller import Users     #引用自創類別，假裝是輸入方的指令(針對多個使用者)
from user_controller import User     #引用自創類別，假裝是輸入方的指令(針對多個使用者)


app = Flask(__name__)
api = Api(app)                  #做一個api變數，引用python flask_restful中的套件 Api 函式


api.add_resource(Users , "/users")    # 為我們api也就是app變數，新增指令
                                      #這段程式碼在說，當我到了https://....../users會執行
                                      # user_controller在Users這個類別(這個有sssssss)
                                      
api.add_resource(User , "/users/<id>")      #這段程式碼在說，當我到了https://....../users/<網址輸入的id>會執行
                                            #user_controller在Users這個類別(這個沒s~~~~~)

@app.route('/') 

def index():
    return "Hello World"

if __name__ == "__main__":    
    app.debug = True          
    app.run(host = '127.0.0.1',port = 5000)  