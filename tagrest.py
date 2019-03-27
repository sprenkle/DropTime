from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
from configuration import Configuration
import collections
import sys

# 67460e74-02e3-11e8-b443-00163e990bdb

db_connect = create_engine('sqlite:///droptime.db')
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
last_seen_tag = None


class UsersList(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from users")  # This line performs query and returns json result
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['userid'] = row[0]
            d['first'] = row[1]
            d['last'] = row[2]
            d['username'] = row[3]
            d['userpassword'] = row[4]
            objects_list.append(d)
        users = {"users": objects_list}
        return users

    def post(self):
        user = request.json
        print(user)
        print(user["first"])
        print(user["last"])
        print(user["username"])
        print(user["userpassword"])
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO users (first, last, username, userpassword)VALUES ('{}','{}','{}','{}')" \
            .format(user["first"], user["last"], user["username"], user["userpassword"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})


class Users(Resource):
    def get(self, user_id):
        conn = db_connect.connect()  # connect to database
        query = conn.execute(
            "select * from users where userid={}".format(user_id))  # This line performs query and returns json result
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['userid'] = row[0]
            d['first'] = row[1]
            d['last'] = row[2]
            d['username'] = row[3]
            d['userpassword'] = row[4]
            objects_list.append(d)
        return objects_list[0]

    def put(self, user_id):
        user = request.json
        print(user)
        conn = db_connect.connect()  # connect to database
        querystring = "Update users set username='{}', userpassword='{}' where Userid={}" \
            .format(user["username"], user["userpassword"], user_id)
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})


class Devices(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from devices")  # This line performs query and returns json result
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['deviceid'] = row[0]
            d['name'] = row[1]
            d['description'] = row[2]
            objects_list.append(d)
        devices = {"devices": objects_list}
        return devices  # Fetches first column that is Employee ID

    def post(self):
        device = request.json
        print(device)
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO devices (name, description) VALUES ('{}','{}')" \
            .format(device["name"], device["description"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})


class Tags(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from tags")  # This line performs query and returns json result
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['tagid'] = row[0]
            d['userid'] = row[1]
            d['name'] = row[2]
            d['description'] = row[3]
            objects_list.append(d)
        tags = {"tags": objects_list}
        return tags  # Fetches first column that is Employee ID

    def post(self):
        tag = request.json
        print(tag)
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO tags (tagid, userid, name, description) VALUES ('{}','{}','{}','{}')" \
            .format(tag["tagid"], tag["userid"], tag["name"], tag["description"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})


class Activities(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from activities")  # This line performs query and returns json result
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['userid'] = row[1]
            d['name'] = row[2]
            d['color'] = row[3]
            d['show'] = row[4]
            d['integration'] = row[5]
            d['dailygoals'] = row[6]
            d['dailytimeSec'] = row[7]
            objects_list.append(d)
        activities = {"activities": objects_list}
        return activities  # Fetches first column that is Employee ID

    def post(self):
        activity = request.json
        print(activity)
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO activities (userid, name, color, show, integration, dailygoals, dailytimeSec) VALUES ('{}','{}','{}','{}','{}','{}','{}')" \
            .format(activity["userid"], activity["name"], activity["color"], activity["show"], activity["integration"],
                    activity["dailygoals"], activity["dailytimeSec"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})


# {"userid":"", "start":"", "stop":"", "showled":"", "sunday":"",
# "monday":"", "tuesday":"", "wednesday":"", "thursday":"", "friday":"", "saturday":"",
# "integration":""}
class Reminders(Resource):
    def get(self, reminder_id):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from reminders where reminderid={}".format(
            reminder_id))  # This line performs query and returns json result
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['userid'] = row[1]
            d['start'] = row[2]
            d['stop'] = row[3]
            d['showled'] = row[4]
            d['sunday'] = row[5]
            d['monday'] = row[6]
            d['tuesday'] = row[7]
            d['wednesday'] = row[8]
            d['thursday'] = row[9]
            d['friday'] = row[10]
            d['saturday'] = row[11]
            d['integration'] = row[12]

            objects_list.append(d)
        return objects_list[0]

    def put(self, reminder_id):
        reminder = request.json
        print(reminder)
        conn = db_connect.connect()  # connect to database
        querystring = "Update reminders set userid={}, start='{}'," \
                      "stop='{}', showled={}, sunday={}, monday={}, tuesday={}," \
                      "wednesday={}, thursday={}, friday={}, saturday={}, integration={} " \
                      "where reminderid={}" \
            .format(reminder["userid"], reminder["start"],
                    reminder["stop"], reminder["showled"], reminder["sunday"],
                    reminder["monday"],
                    reminder["tuesday"], reminder["wednesday"], reminder["thursday"],
                    reminder["friday"], reminder["saturday"], reminder["integration"],
                    reminder_id)
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})


class LastSeenTag(Resource):
    def get(self):
        return last_seen_tag


class TagsToActionsList(Resource):

    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from tagstoactions")  # This line performs query and returns json result
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['tagid'] = row[0]
            d['actiontype'] = row[1]
            d['identifier'] = row[2]
            objects_list.append(d)
        tags_to_actions = {"tagstoactions": objects_list}
        return tags_to_actions


class TagsToActions(Resource):

    def get(self, action_type, tag_id):
        global last_seen_tag
        if tag_id is not None:
            last_seen_tag = tag_id
        print(tag_id)
        conn = db_connect.connect()  # connect to database
        query_string = "select tta.tagid, tta.actiontype, tta.identifier, t.userid from tagstoactions tta join tags t on tta.tagid = t.tagid where tta.tagid = '{}' and actiontype='{}'".format(
            tag_id, action_type)
        print(query_string)
        query = conn.execute(query_string)
        objects_list = []
        for row in query.cursor:
            d = collections.OrderedDict()
            d['tagid'] = row[0]
            d['actiontype'] = row[1]
            d['identifier'] = row[2]
            d['userid'] = row[3]
            objects_list.append(d)
        if len(objects_list) == 0:
            return None
        return objects_list[0]

    def post(self):
        tagtoaction = request.json
        print(tagtoaction)
        conn = db_connect.connect()  # connect to database
        querystring = "INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES ('{}','{}','{}')" \
            .format(tagtoaction["tagid"], tagtoaction["actiontype"], tagtoaction["identifier"])
        conn.execute(querystring)  # This line performs query and returns json result
        return jsonify({"results": "ok"})


api.add_resource(LastSeenTag, '/lastseentag')  # Route_1
api.add_resource(TagsToActionsList, '/tagstoactions')  # Route_1
api.add_resource(TagsToActions, '/tagstoactions', '/tagstoactions/<type>/<string:tag_id>')  # Route_1
api.add_resource(UsersList, '/users')  # Route_1UsersUpdate
api.add_resource(Users, '/users/<user_id>')  # Route_1
api.add_resource(Devices, '/devices')  # Route_1
api.add_resource(Tags, '/tags')  # Route_1
api.add_resource(Activities, '/activities')  # Route_1
api.add_resource(Reminders, '/reminders/<reminder_id>')  # Route_1

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        file = "debug_config.json"
    else:
        file = "configuration.json"

    configuration = Configuration(file)
    url = configuration.get_value("tag_api", "self_url")
    print("Url is {}".format(url))
    app.run(host=url, port='5002')