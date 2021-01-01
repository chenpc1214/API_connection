from flask import Flask,jsonify,request
from flask_restful import Api
from merge_users import Users     #引用自創類別，假裝是輸入方的指令(針對多個使用者)
from merge_user import User     #引用自創類別，假裝是輸入方的指令(針對多個使用者)
from merge_account import account_controller,one_controller
import pymysql
import traceback
import jwt                       #驗證系統(json_web_token)
import time
from server import app           #從自建serve.py 引進 SQLAlchemy


app = Flask(__name__)
api = Api(app)                  #做一個api變數，引用python flask_restful中的套件 Api 函式


api.add_resource(Users , "/users")    # 為我們api也就是app變數，新增指令
                                      #這段程式碼在說，當我到了https://....../users會執行
                                      # user_controller在Users這個類別(這個有sssssss)
                                      
api.add_resource(User , "/users/<id>")      #這段程式碼在說，當我到了https://....../users/<網址輸入的id>會執行
                                            #user_controller在Users這個類別(這個沒s~~~~~)
                                            
api.add_resource(account_controller , "/users/<user_id>/accounts")
api.add_resource(one_controller , "/users/<user_id>/accounts/<id>")

@app.errorhandler(Exception)
def handler_error(error):
    status_code =500
    if type(error).__name__ == "NotFound":
        status_code =404
    elif type(error).__name__ =="TypeErro":
        status_code =500
    return jsonify({'msg:':type(error).__name__}),status_code

@app.before_request                         #別人要進到我家(網址)之前要先經過驗證
#def auth():
#    token = request.headers.get('auth')     #檢查headers
#    user_id = request.get_json()['user_id']   #規定使用者要以json格式，且用鍵為user_id方式傳值進來
    
#    valid_token = jwt.encode({'user_id':user_id,"timestamp":int(time.time())}, 
#                            'password',
#                            algorithm='HS256')                                 #jwt可以將使用者傳來的資料，和現在時間點
                                                                               #產出一個亂碼，確定使用者身分
                                                                               #(每經過一秒會重新再次加密)
                                                                               #password是要加密使用者傳來的資料
                                                                               #它是一種金鑰，可能會根據使用者的id
                                                                               #從資料庫取得該使用者專屬的金鑰
#    print(valid_token)
#    if token==valid_token:
#        pass
#    else:
#        return{
#            'msg':'invalid token'
#        }
                                        
    
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
    