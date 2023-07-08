from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify, request
import bson.json_util as json_util
from bson import ObjectId
from flask_restful import Resource, Api


app = Flask(__name__)

api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/UserData"
mongo = PyMongo(app)

class flaskapp(Resource):

    def __init__(self):
        pass

    def get(self, id):
        user = mongo.db.Users.find({"_id":ObjectId(id)})
        data = list(user)
        resp = jsonify(str(data))
        return resp
           
    def put(self, id):
        data = request.get_json()
        Name = data['name']
        Email = data['email']
        Password = data['password']

        mongo.db.Users.update_one({"_id":ObjectId(id)}, {"$set":{"name":Name,"email":Email,"password":Password}})
        
        resp = jsonify("User updated successfully")
        return resp
    
    def delete(self, id):
        num = ObjectId(id)
        mongo.db.Users.delete_one({"_id": num})
        resp = jsonify("User deleted successfully")
        return resp
    
class getusers(Resource):

    def __init__(self):
        pass

    def get(self):
        user = mongo.db.Users.find()
        data = list(user)
        resp = jsonify(str(data))
        return resp
    
    def post(self):
        data = request.get_json()
        Name = data['name']
        Email = data['email']
        Password = data['password']

        mongo.db.Users.insert_one({"name": Name, 
                                    "email": Email, 
                                    "password": Password})
        
        resp = jsonify("user added successfully")
        return resp
    
    
api.add_resource(flaskapp, '/<string:id>')
api.add_resource(getusers, '/')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
