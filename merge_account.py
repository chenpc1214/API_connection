from flask_restful import Resource
from flask_restful import reqparse 
from flask import jsonify            
import pymysql                       
import traceback 

parser = reqparse.RequestParser()

parser.add_argument('id')              
parser.add_argument('balance')            
parser.add_argument('account_number')             
parser.add_argument('user_id')                                 

class account_controller(Resource):
    
    def db_init(self):
        db = pymysql.connect("localhost","root","asd23029663","account")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        return db,cursor
    
    def get(self,user_id):                                   #合併路徑，必須提供它對映的路徑
        db,cursor=self.db_init()
        sql = "SELECT * FROM account.myaccount WHERE user_id='{}' and  deleted is not True".format(user_id)

        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()
        
        return jsonify({"data":users})                    #要以{"data":users}方式帶入，畢竟人家是json
    
    def post(self,user_id):
        db,cursor=self.db_init()
        myarg = parser.parse_args()
        
        users = {                                                                                                                                              
            'balance':myarg['balance'],
            'account_number':myarg['account_number'],                         
            'user_id':myarg['user_id']                 
        }
        
        sql = """INSERT INTO account.myaccount ( `balance`, `account_number`, `user_id`) VALUES ( '{}', '{}', '{}');
        """.format(users['balance'],users['account_number'],users['user_id']) 
        
        response = {}
        
        try:                                               
            cursor.execute(sql)
            response['msg'] = 'success'
            
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
            
        db.commit()
        db.close
        return jsonify(response)
    
class one_controller(Resource):
    
    def db_init(self):
        db = pymysql.connect("localhost","root","asd23029663","account")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    
    def get(self,user_id):                                                     #參數列要多加id這參數
        db, cursor =self.db_init()                                        
        sql ="""Select * from account.myaccount WHERE id = '{}' and deleted is not True""".format(id)                          
        cursor.execute(sql)                                        
        db.commit()                                                
        user= cursor.fetchone()
        db.close()
        
        return jsonify({"data": user})
    
    def patch(self,user_id,id):                                             
        
        db, cursor =self.db_init()
        query = []                                                
        
        myarg = parser.parse_args()
        
        user= {  
            'id':myarg['id'],                                                                       
            'balance':myarg['balance'],
            'account_number':myarg['account_number'],                         
            'user_id':myarg['user_id']                  
        }
        
        for key , value in user.items():                           
            if value != None:                                      
                query.append(key + "=" + " '{}' ".format(value))   
        
        query = "," .join(query)
        
        sql = """ UPDATE account.myaccount SET {} WHERE(id = '{}')   
        """.format(query , id)
        
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
    
    def delete(self,user_id):
        db, cursor =self.db_init()
        sql =  """ UPDATE account.myaccount SET deleted=True WHERE (id='{}')
        """.format(id)
        
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