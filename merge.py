from flask import Flask,jsonify,request
from flask_restful import Api
from merge_users import Users     #引用自創類別，假裝是輸入方的指令(針對多個使用者)
from merge_user import User     #引用自創類別，假裝是輸入方的指令(針對多個使用者)
from merge_account import account_controller,one_controller
import pymysql
import traceback


app = Flask(__name__)
api = Api(app)                  #做一個api變數，引用python flask_restful中的套件 Api 函式


api.add_resource(Users , "/users")    # 為我們api也就是app變數，新增指令
                                      #這段程式碼在說，當我到了https://....../users會執行
                                      # user_controller在Users這個類別(這個有sssssss)
                                      
api.add_resource(User , "/users/<id>")      #這段程式碼在說，當我到了https://....../users/<網址輸入的id>會執行
                                            #user_controller在Users這個類別(這個沒s~~~~~)
                                            
api.add_resource(account_controller , "/users/<user_id>/accounts")
api.add_resource(one_controller , "/users/<user_id>/accounts/<id>")

@app.route('/') 


def index():
    return "Hello World"


@app.route("/users/<user_id>/accounts/<id>/deposit",methods=['POST'])  #表示此網址，只會用post進行

def deposit(user_id,id):                              #存錢系統
    db,cursor,account = get_account(id)
    money = request.get_json()['money']               #使用request去解析網址參數，
                                                      #並以json方式解析money這從網頁進來的資料
    balance = account['balance']+int(money)
    
    sql = "update account.myaccount set balance = {} where id={} and deleted is not True".format(balance,id)
    response = {}
        
    try:                                               
        cursor.execute(sql)
        response['msg'] = 'success'
            
    except:
        traceback.print_exc()
        response['msg'] = 'failed'
            
    db.commit()
    db.close()
    return jsonify(response)

@app.route("/users/<user_id>/accounts/<id>/withdraw",methods=['POST'])  #表示此網址，只會用post進行

def withdraw(user_id,id):                              #領錢系統
    db,cursor,account = get_account(id)
    money = request.get_json()['money']               #使用request去解析網址參數，
                                                      #並以json方式解析money這從網頁進來的資料
    balance = account['balance']-int(money)
    
    response = {}
    
    if balance< 0:                                     #防呆機制
        response['msg'] = "no money can withdraw"
        return jsonify(response)                        #既然有錯後續就不用執行......
    
    else:

        sql = "update account.myaccount set balance = {} where id={} and deleted is not True".format(balance,id)
        
        try:                                               
            cursor.execute(sql)
            response['msg'] = 'success'
                
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
                
        db.commit()
        db.close()
        return jsonify(response)

def get_account(id):
    db = pymysql.connect("localhost","root","asd23029663","account")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """select * from account.myaccount where id ='{}' and deleted is not True""".format(id)
    cursor.execute(sql)
    return db, cursor,cursor.fetchone()

if __name__ == "__main__":    
    app.debug = True          
    app.run(host = '127.0.0.1',port = 5000) 
    