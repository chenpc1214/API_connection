#資料庫模型區

from server import db

class UserModel(db.Model):
    __tablename__='users'    #要連到資料庫哪一張表
    
    id = db.Column(db.Integer,primary_key=True)      #定義欄位
    name =db.Column(db.String(45))
    gender =db.Column(db.Integer)
    birth =db.Column(db.DateTime)
    note =db.Column(db.Text)
    deleted = db.Column(db.Boolean)
    
    def __init__(self,name,gender,birth,note,deleted=None):   #初始化
        self.name = name                                      #賦值項目可更改成自己喜歡的名子
        self.gender = gender                                  #同上
        self.birth = birth                                    #同上
        self.note = note                                      #同上
        self.deleted = deleted                                #同上
        
    def serialize(self):                                      #用來解決api回傳型態(json格式)                             
        return{                                               #與SQLAlchemy型態不同的問題
            "name":self.name,
            "gender":self.gender,                         
            "birth ":self.birth ,
            "note":self.note,
            "deleted":self.deleted,
            }                                                    
        
                                                             