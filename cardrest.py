from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from flask_jsonpify import jsonify

db_connect = create_engine('sqlite:///droptime.db')
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

class Users(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from users")  # This line performs query and returns json result
        return {'users': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

    def post(self, id):
        print(id)
        user = request.json
        print(user["first"])
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO users (first, last, username, userpassword)VALUES ('{}','{}','{}','{}')"\
            .format(user["first"], user["last"], user["username"], user["userpassword"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})

class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(Users, '/users/<string:id>', '/users')  # Route_1
api.add_resource(Tracks, '/tracks')  # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3

if __name__ == '__main__':
    app.run(port='5002')

