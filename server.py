from flask import Flask
from flask_restful import Api

from Cooker import Cooker
from Session import Session
from Loginer import Loginer
from Register import Register
from CreateOrder import CreateOrder
from Menu import Menu
from Status import Status
from Change import Change
from Adder import Adder

# initialization of app and RESTful api
app = Flask(__name__)
api = Api()
users = []

# add handlers
api.add_resource(Session, "/api/session")
api.add_resource(Loginer, "/api/login")
api.add_resource(Register, "/api/register")
api.add_resource(Menu, "/api/menu")
api.add_resource(CreateOrder, "/api/create_order")
api.add_resource(Cooker, "/api/cook")
api.add_resource(Status, "/api/status")
api.add_resource(Change, "/api/change")
api.add_resource(Adder, "/api/add")
api.init_app(app)

# run server on localhost
app.run(debug=True, port=3000, host="localhost")
