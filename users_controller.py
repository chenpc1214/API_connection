from flask_restful import Resource
from flask_restful import reqparse   #用來處理使用者的post來的資料
from flask import jsonify            #用來將我們從資料庫取出的資料，自動整合成json格式
import pymysql                       #用來連資料庫的套件
import traceback                     #印出錯誤訊息的套件

parser = reqparse.RequestParser()    #做一個篩子，當使用者丟一堆資料過來，我只選我要的

parser.add_argument('name')              #要留下的東西
parser.add_argument('gender')            #同上
parser.add_argument('birth')             #同上
parser.add_argument('note')              #同上




class Users(Resource):                                                #針對多筆資料
    
    def db_init(self):                                                #初始化
        db = pymysql.connect("localhost","root","asd23029663","api")  #連線資料庫，(資料庫主機位置、帳號、密碼、資料庫名稱)
        cursor = db.cursor(pymysql.cursors.DictCursor)                #這行功能在於當有資料庫的資料被取出，例如：id:25 name:John
                                                                      #沒有此段敘述，就會這樣顯示---> {25 , "john"}，會不知道欄位名
        return db , cursor
    
    def get(self):
        db, cursor =self.db_init()                                  #準備好資料庫、和取出的資料
        sql = """Select * from api.users WHERE deleted is not True"""  #軟刪除方式所以用此語法
        cursor.execute(sql)                                        
        db.commit()                                                #送出指令
        users = cursor.fetchall()                                  #取道資料後，放到user變數中
        db.close()
        
        return jsonify({"data": users})
    
    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()                                  # 將使用者傳來的資料，放到變數arg中，資料結構是鍵值所構成
        
        users = {                                                    #方便做資料的改動與設定                       
            'name':arg['name'],
            'gender':arg['gender'] or 0,                            #沒輸入就是預設值 0 
            'birth':arg['birth'] or '1900-01-01',                   #沒輸入就是預設值 '1900-01-01' 
            'note':arg['note']
        }
        
        sql = """
        INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        """ .format(users['name'],users['gender'],users['birth'],users['note'])
        
        response = {}
        
        try:                                               #非讀的的資料都要經過驗證或檢查
            cursor.execute(sql)
            response['msg'] = 'success'
            
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
            
        db.commit()
        db.close
        return jsonify(response)