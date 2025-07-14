from flask import Flask
from flask_restful import Api
from resources.item import Item

app = Flask(__name__)

api = Api(app)

items = [] #DB의 대체역할 (간단한 DB역할)

api.add_resource(Item, '/item/<string:name>') #경로 추가

if __name__ =="__main__":
    app.run(debug=True)