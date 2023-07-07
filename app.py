from json import dumps
from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify, request
import bson.json_util as json_util
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/UserData"
mongo = PyMongo(app)

@app.route('/add', methods = ['POST'])
def adduser():
    data = request.get_json()
    Name = data['name']
    Email = data['email']
    Password = data['password']

    mongo.db.Users.insert_one({"name": Name, 
                                  "email": Email, 
                                  "password": Password})
    
    resp = jsonify("user added successfully")
    return resp

@app.route('/details')
def allusers():
    user = mongo.db.Users.find()
    data = list(user)
    resp = json_util.dumps(data)
    return resp

@app.route('/details/<id>')
def getuser(id): 
    user = mongo.db.Users.find_one({"_id": ObjectId(id)})
    # data = list(user)
    resp = json_util.dumps(user)
    return resp

@app.route('/update/<id>', methods=['PUT'])
def updateuser(id):
    data = request.get_json()
    Name = data['name']
    Email = data['email']
    Password = data['password']

    mongo.db.Users.update_one({"_id":ObjectId(id)}, {"$set":{"name":Name,"email":Email,"password":Password}})
    
    resp = jsonify("User updated successfully")
    return resp

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    mongo.db.Users.delete_one({"_id": ObjectId(id)})
    resp = jsonify("User deleted successfully")
    return resp

if __name__ == "__main__":
    app.run(debug=True, port=5000)