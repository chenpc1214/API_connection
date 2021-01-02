#SQLAlchemy伺服器......
#將原來的@app和資料庫提出來，與以往用pymysql建立一個db的不同處在於
# SQLAlchemy可以讓此檔的db讓不同py檔案使用

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/api'  #設定資料庫的連結
                                                                                            #root使用者名稱
                                                                                            #localhost資料庫主機位置
                                                                                            #api為資料庫名稱
db = SQLAlchemy(app)