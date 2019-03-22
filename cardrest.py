from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
import uuid
# 67460e74-02e3-11e8-b443-00163e990bdb

db_connect = create_engine('sqlite:///droptime.db')
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

class Users(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from users")  # This line performs query and returns json result
        return {'users': [i for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

    def post(self):
        user = request.json
        print(user)
        print(user["first"])
        print(user["last"])
        print(user["username"])
        print(user["userpassword"])
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO users (first, last, username, userpassword)VALUES ('{}','{}','{}','{}')"\
            .format(user["first"], user["last"], user["username"], user["userpassword"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})

class Devices(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from devices")  # This line performs query and returns json result
        return {'devices': [i for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

    def post(self):
        device = request.json
        print(device)
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO devices (name, description) VALUES ('{}','{}')"\
            .format(device["name"], device["description"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})



api.add_resource(Users, '/users')  # Route_1
api.add_resource(Devices, '/devices')  # Route_1


if __name__ == '__main__':
    app.run(port='5002')

