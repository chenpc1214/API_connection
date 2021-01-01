from flask import Flask
from flask_restful import Api
from class_account import account_controller,one_controller

myaccount = Flask(__name__)
myapi = Api(myaccount)

myapi.add_resource(account_controller , "/accounts")
myapi.add_resource(one_controller , "/accounts/<id>")


@myaccount.route("/")

def index():
    return "this is my private space"
if __name__ == "__main__":    
    myaccount.debug = True          
    myaccount.run(host = '127.0.0.1',port = 5000)