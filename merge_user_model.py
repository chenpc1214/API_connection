from flask_restful import Resource
from flask_restful import reqparse                 #用來處理使用者的post來的資料
from flask import jsonify,make_response            #jsonify用來將我們從資料庫取出的資料，自動整合成json格式
                                                   #在restful當中，return型態是jsonify，但是它是在一個物件內
                                                   #結構比較特殊
import pymysql                       #用來連資料庫的套件
import traceback                     #印出錯誤訊息的套件

from server import db
from models import UserModel


parser = reqparse.RequestParser()    #做一個篩子，當使用者丟一堆資料過來，我只選我要的

parser.add_argument('name')              #要留下的東西
parser.add_argument('gender')            #同上
parser.add_argument('birth')             #同上
parser.add_argument('note')              #同上



class Users(Resource):                                                #針對多筆資料
    
    def db_init(self):                                                #初始化
        db = pymysql.connect("localhost","root","***********","api")  #連線資料庫，(資料庫主機位置、帳號、密碼、資料庫名稱)
        cursor = db.cursor(pymysql.cursors.DictCursor)                #這行功能在於當有資料庫的資料被取出，例如：id:25 name:John
                                                                      #沒有此段敘述，就會這樣顯示---> {25 , "john"}，會不知道欄位名
        return db , cursor
    
    def get(self):
        user = UserModel.query.filter(UserModel.deleted.isnot(True).all)
        return jsonify({"data":list(map(lambda users:user.serialize))})
    
    def post(self):
        
        arg = parser.parse_args() 
        users = {                                                    #方便做資料的改動與設定                       
            'name':arg['name'],
            'gender':arg['gender'],                            #沒輸入就是預設值 0 
            'birth':arg['birth'],                             #沒輸入就是預設值 '1900-01-01' 
            'note':arg['note']
        }
        
        response = {}
        status_code = 200
        
        try:                               
            new_user = UserModel(name = users['name'],gender=users['gender'],birth=users['birth'],note=users['note'])
            db.session.add(new_user)
            db.session.commit()
        
            response['msg'] = 'success'
            
        except:
            status_code =400
            traceback.print_exc()
            response['msg'] = 'failed'
            
        
        return  make_response(jsonify(response),status_code)


class User(Resource):                                                #針對多筆資料
    
    def db_init(self):                                                #初始化
        db = pymysql.connect("localhost","root","asd23029663","api")  #連線資料庫，(資料庫主機位置、帳號、密碼、資料庫名稱)
        cursor = db.cursor(pymysql.cursors.DictCursor)                #這行功能在於當有資料庫的資料被取出，例如：id:25 name:John
                                                                      #沒有此段敘述，就會這樣顯示---> {25 , "john"}，會不知道欄位名
        return db , cursor
    
    def get(self,id):                                                     #參數列要多加id這參數
        db, cursor =self.db_init()                                        #因為要單一一筆要用where
        sql ="""Select * from api.users WHERE id = '{}' and   deleted is not True""".format(id)  #軟刪除方式                         
        cursor.execute(sql)                                        
        db.commit()                                                
        user = cursor.fetchone()                                    #改成fetchone
        db.close()
        
        return jsonify({"data": user})
    
    def patch(self,id):                                             #小部分更改資料
        
        db, cursor =self.db_init()
        query = []                                                 #剖析傳來的資料
        
        arg = parser.parse_args()                                  # 將使用者傳來的資料，放到變數arg中，資料結構是鍵值所構成
        
        user = {                                                    #方便做資料的改動與設定                       
            'name':arg['name'],
            'gender':arg['gender'] ,                       
            'birth':arg['birth'],
            'note':arg['note']
        }
        
        for key , value in user.items():                           #將接收來的資料，拆成鍵值兩部分
            if value != None:                                      #假使用者有未填的部分
                query.append(key + "=" + " '{}' ".format(value))   #去除那個未填寫的部分，其餘加到陣列中
        
        query = "," .join(query)
        
        sql = """ UPDATE api.users SET {} WHERE(id = '{}')   
        """.format(query , id)
        
        response = {}
        
        try:                                               #非讀的的資料都要經過驗證或檢查
            cursor.execute(sql)
            response['msg'] = 'success'
            
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
            
        db.commit()
        db.close()
        return jsonify(response)
    
    def delete(self,id):
        db, cursor =self.db_init()
        sql =  """ UPDATE api.users SET deleted=True WHERE (id='{}')
        """.format(id)
        
        response = {}
        status_code = 200
        try:                                               #非讀的的資料都要經過驗證或檢查
            cursor.execute(sql)
            response['msg'] = 'success'
            
        except:
            status_code =400
            traceback.print_exc()
            response['msg'] = 'failed'
            
        db.commit()
        db.close()
        return  make_response(jsonify(response),status_code)
        
        