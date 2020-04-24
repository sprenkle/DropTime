from flask import Flask, request
from flask_restful import Resource, Api, reqparse
# from sqlalchemy import create_engine
import sqlite3
from flask_jsonpify import jsonify
from configuration import Configuration
import collections
import sys
import uuid
from datetime import datetime
from flask_cors import CORS, cross_origin

# uuid.uuid4()
# 67460e74-02e3-11e8-b443-00163e990bdb
# eb339b2f-c43b-4278-a95d-38d17828cb3f
# 90fa5fe2-953d-4ae8-97c5-a4bcadfc3178

#db_connect = create_engine('sqlite:///droptime.db')
app = Flask(__name__)

api = Api(app)
CORS(app)

parser = reqparse.RequestParser()
last_seen_tag = None
last_device = None


class UsersList(Resource):
    def get(self):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        query = conn.execute("select * from users")  # This line performs query and returns json result
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['userid'] = row[0]
            d['first'] = row[1]
            d['last'] = row[2]
            d['username'] = row[3]
            d['userpassword'] = row[4]
            objects_list.append(d)
        users = {"users": objects_list}
        db_connect.close()
        return users

    def post(self):
        user = request.json
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        querystring = "INSERT INTO users (first, last, username, userpassword)VALUES ('{}','{}','{}','{}','{}')" \
            .format(user["first"], user["last"], user["username"], user["userpassword"])
        conn.execute(querystring)  # This line performs query and returns json result
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok"})


class Users(Resource):
    def get(self, user_id):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()

        #conn = db_connect.connect()  # connect to database
        query = conn.execute(
            "select * from users where userid='{}'".format(user_id))  # This line performs query and returns json result
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['userid'] = row[0]
            d['first'] = row[1]
            d['last'] = row[2]
            d['username'] = row[3]
            d['userpassword'] = row[4]
            objects_list.append(d)
        db_connect.close()
        return objects_list[0]

    def put(self, user_id):
        user = request.json
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        querystring = "Update users set username='{}', userpassword='{}' where Userid='{}'" \
            .format(user["username"], user["userpassword"], user_id)
        conn.execute(querystring)  # This line performs query and returns json result
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok"})


class Devices(Resource):
    def get(self):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        query = conn.execute("select * from devices")  # This line performs query and returns json result
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['deviceid'] = row[0]
            d['name'] = row[1]
            d['description'] = row[2]
            objects_list.append(d)
        devices = {"devices": objects_list}
        db_connect.close()
        return devices  # Fetches first column that is Employee ID

    def post(self):
        device = request.json
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        device_id = uuid.uuid4()
        querystring = "INSERT INTO devices (deviceid, name, description) VALUES ('{}','{}','{}')" \
            .format(device_id, device["name"], device["description"])
        conn.execute(querystring)  # This line performs query and returns json result
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok", "id": device_id})


class Tag(Resource):
    def get(self, tag_id):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        sql = f"select * from tags where tagid={tag_id}"
        query = conn.execute(f"select * from tags where tagid={tag_id}")
        print(sql)
        d = collections.OrderedDict()
        for row in query:
            d = collections.OrderedDict()
            d['tagid'] = row[0]
            d['userid'] = row[1]
            d['name'] = row[2]
            d['description'] = row[3]
        db_connect.close()
        return d  # Fetches first column that is Employee ID

    def post(self):
        tag = request.json
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        # tag_id = uuid.uuid4()
        # ON CONFLICT(tagid) DO UPDATE SET userid='{}', name='{}', description='{}'"
        querystring = "INSERT INTO tags (tagid, userid, name, description) VALUES ( {},'{}','{}','{}' )" \
            .format(tag["tagid"], tag["userid"], tag["name"], tag["description"])
        print(querystring)
        try:
            out = conn.execute(querystring)
            print(out)
        except Exception as e:
            querystring = "UPDATE tags SET userid='{}', name='{}', description='{}' where tagid={}" \
                .format(tag["userid"], tag["name"], tag["description"], tag["tagid"])
            print(querystring)
            conn.execute(querystring)  # This line performs query and returns json result
        db_connect.commit();
        db_connect.close()
        return jsonify({"results": "ok", "id": tag["tagid"]})

    def delete(self, tag_id):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        sql = f"delete from tags where tagid={tag_id}"
        conn.execute(sql)
        db_connect.commit()
        db_connect.close()


class Tags(Resource):
    def get(self, user_id=None):
        db_connect = sqlite3.connect('droptime.db')
        c = db_connect.cursor()

        if user_id is None:
            query = c.execute("select * from tags")  # This line performs query and returns json result
        else:
            query = c.execute("select * from tags where userid='" + user_id + "'")  # This line performs query and returns json result

        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['tagid'] = row[0]
            d['userid'] = row[1]
            d['name'] = row[2]
            d['description'] = row[3]
            objects_list.append(d)
        tags = {"tags": objects_list}
        db_connect.close()
        return tags  # Fetches first column that is Employee ID


    def post(self):
        tag = request.json
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        tag_id = uuid.uuid4()
        querystring = "INSERT INTO tags (tagid, userid, name, description) VALUES ('{}','{}','{}','{}')" \
            .format(tag_id, tag["userid"], tag["name"], tag["description"])
        conn.execute(querystring)  # This line performs query and returns json result
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok", "id": tag_id})


class Activities(Resource):

    def get(self, activity_id=None):
        if activity_id is None:
            db_connect = sqlite3.connect('droptime.db')
            conn = db_connect.cursor()
            query = conn.execute("select * from activities")  # This line performs query and returns json result
            objects_list = []
            for row in query:
                d = collections.OrderedDict()
                d['activityid'] = row[0]
                d['userid'] = row[1]
                d['name'] = row[2]
                d['color'] = row[3]
                d['show'] = row[4]
                d['dailyGoals'] = row[5]
                d['dailytimeSec'] = row[6]
                objects_list.append(d)
            activities = {"activities": objects_list}
            db_connect.close()
            return activities  # Fetches first column that is Employee ID
        else:
            db_connect = sqlite3.connect('droptime.db')
            conn = db_connect.cursor()
            query = conn.execute("select * from activities where activityid={}".format(
                activity_id))  # This line performs query and returns json result
            objects_list = []
            activities = None
            for row in query:
                d = collections.OrderedDict()
                d['activityid'] = row[0]
                d['userid'] = row[1]
                d['name'] = row[2]
                d['color'] = row[3]
                d['show'] = row[4]
                d['dailyGoals'] = row[5]
                d['dailytimeSec'] = row[6]
                objects_list.append(d)
            if len(objects_list) > 0:
                activities = objects_list[0]
            db_connect.close()
            return activities  # Fetches first column that is Employee ID

    def post(self):
        activity = request.json
        print(activity)
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        querystring = "INSERT INTO activities (activityid, userid, name, color, show, " \
                      "dailyGoals, dailytimeSec) VALUES ('{}','{}','{}','{}','{}','{}','{}')" \
            .format(activity["activityid"], activity["userid"], activity["name"], activity["color"], activity["show"],
                    activity["dailyGoals"], activity["dailytimeSec"])
        try:
            conn.execute(querystring)  # This line performs query and returns json result
        except Exception as e:
            querystring = "UPDATE activities set userid = '{}', name = '{}', color = '{}', show = '{}', " \
                          "dailyGoals = {}, dailytimeSec = {} where activityid = {}" \
                .format(activity["userid"], activity["name"], activity["color"], activity["show"],
                        activity["dailyGoals"], activity["dailytimeSec"], activity["activityid"])
            conn.execute(querystring)  # This line performs query and returns json result
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok"})


class ActivitiesList(Resource):

    def get(self):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        query = conn.execute("select * from activities")  # This line performs query and returns json result
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['activityid'] = row[0]
            d['userid'] = row[1]
            d['name'] = row[2]
            d['color'] = row[3]
            d['show'] = row[4]
            d['dailyGoals'] = row[5]
            d['dailytimeSec'] = row[6]
            objects_list.append(d)
        activities = {"activities": objects_list}
        db_connect.close()
        return activities  # Fetches first column that is Employee ID



# {"userid":"", "start":"", "stop":"", "showled":"", "sunday":"",
# "monday":"", "tuesday":"", "wednesday":"", "thursday":"", "friday":"", "saturday":"",
# "integration":""}
class Reminders(Resource):
    def get(self, user_id):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()

        sql = "select reminderid, name,userid,deviceid,start,duration,showled,sunday,monday," \
                             "tuesday,wednesday,thursday,friday,saturday from reminders" \
                             " where userid = '{}'".format(user_id)
        print(sql)
        query = conn.execute(sql)
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['reminderid'] = row[0]
            d['name'] = row[1]
            d['userid'] = row[2]
            d['deviceid'] = row[3]
            d['start'] = row[4]
            d['duration'] = row[5]
            d['showled'] = row[6]
            d['sunday'] = row[7]
            d['monday'] = row[8]
            d['tuesday'] = row[9]
            d['wednesday'] = row[10]
            d['thursday'] = row[11]
            d['friday'] = row[12]
            d['saturday'] = row[13]
            objects_list.append(d)
        reminders = []
        if len(objects_list) > 0:
            reminders = {"reminders": objects_list}
        db_connect.close()
        return reminders

    def delete(self, reminder_id):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        querystring = "DELETE FROM reminders WHERE reminderid='{}'" \
            .format(reminder_id)
        conn.execute(querystring)
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok"})


    def post(self):
        reminder = request.json

        if reminder["reminderid"] == "0":
            reminder["reminderid"] = uuid.uuid4()

        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        querystring = "INSERT INTO reminders (reminderid, name, userid, deviceid, start," \
                      "duration, showled, sunday, monday, tuesday," \
                      "wednesday, thursday, friday, saturday) VALUES ('{}','{}','{}','{}','{}',{},{}," \
                      "{},{},{},{},{},{},{})" \
            .format(reminder["reminderid"], reminder["name"], reminder["userid"], reminder["deviceid"], reminder["start"],
                    reminder["duration"], reminder["showled"], reminder["sunday"],
                    reminder["monday"],
                    reminder["tuesday"], reminder["wednesday"], reminder["thursday"],
                    reminder["friday"], reminder["saturday"])
        try:
            conn.execute(querystring)
        except Exception as e:
            querystring = "Update reminders set name='{}', userid='{}', deviceid='{}', start='{}'," \
                          "duration={}, showled={}, sunday={}, monday={}, tuesday={}," \
                          "wednesday={}, thursday={}, friday={}, saturday={} " \
                          "where reminderid='{}'" \
                .format(reminder["name"], reminder["userid"], reminder["deviceid"], reminder["start"],
                        reminder["duration"], reminder["showled"], reminder["sunday"],
                        reminder["monday"],
                        reminder["tuesday"], reminder["wednesday"], reminder["thursday"],
                        reminder["friday"], reminder["saturday"], reminder["reminderid"])
            conn.execute(querystring)
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok"})


# class CurrentReminders(Resource):
#
#     def get(self, current_time):
#         db_connect = sqlite3.connect('droptime.db')
#         conn = db_connect.cursor()
#         query = conn.execute("select * from reminders")
#         objects_list = []
#         for row in query:
#             d = collections.OrderedDict()
#             d['reminderid'] = row[0]
#             d['userid'] = row[1]
#             d['start'] = datetime.strptime(row[2], "%Y-%m-%dT%H:%M:%S.000")
#             d['duration'] = row[3]
#             d['showled'] = row[4]
#             d['sunday'] = row[5]
#             d['monday'] = row[6]
#             d['tuesday'] = row[7]
#             d['wednesday'] = row[8]
#             d['thursday'] = row[9]
#             d['friday'] = row[10]
#             d['saturday'] = row[11]
#
#             objects_list.append(d)
#         db_connect.close()
#         return objects_list
#
#     def put(self, reminder_id):
#         reminder = request.json
#         db_connect = sqlite3.connect('droptime.db')
#         conn = db_connect.cursor()
#         querystring = "Update reminders set userid={}, start='{}'," \
#                       "stop='{}', showled={}, sunday={}, monday={}, tuesday={}," \
#                       "wednesday={}, thursday={}, friday={}, saturday={} " \
#                       "where reminderid='{}'" \
#             .format(reminder["userid"], reminder["start"],
#                     reminder["stop"], reminder["showled"], reminder["sunday"],
#                     reminder["monday"],
#                     reminder["tuesday"], reminder["wednesday"], reminder["thursday"],
#                     reminder["friday"], reminder["saturday"],
#                     reminder_id)
#         conn.execute(querystring)  # This line performs query and returns json result
#         db_connect.commit()
#         db_connect.close()
#         return jsonify({"results": "ok"})


class LastSeenTag(Resource):
    def get(self):
        return {"last_tag": last_seen_tag, "last_device": last_device}


class TagsToActionsList(Resource):

    def get(self):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        query = conn.execute("select ta.tagid, ta.actiontype, ta.identifier from tagstoactions ta")  # This line performs query and returns json result
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['tagid'] = row[0]
            d['actiontype'] = row[1]
            d['identifier'] = row[2]
            objects_list.append(d)
        tags_to_actions = {"tagstoactions": objects_list}
        db_connect.close()
        return tags_to_actions


class TagsToActions(Resource):

    def get(self, action_type, tag_id, device_id):
        global last_seen_tag, last_device
        if tag_id is not None:
            last_seen_tag = tag_id
            last_device = device_id
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()

        if(tag_id == None and device_id == None):
            query_string = "select tta.tagid, tta.actiontype, tta.identifier, t.userid from tagstoactions tta join " \
                       "tags t on tta.tagid = t.tagid where tta.tagid = '{}' and actiontype='{}'".format(tag_id,
                                                                                                         action_type)
        query = conn.execute(query_string)
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['tagid'] = row[0]
            d['actiontype'] = row[1]
            d['identifier'] = row[2]
            d['userid'] = row[3]
            objects_list.append(d)
        if len(objects_list) == 0:
            return None
        db_connect.close()
        return objects_list[0]

    def delete(self, action_type, tag_id):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        query_string = "delete from tagstoactions where tagid = '{}' and actiontype='{}'"\
            .format(tag_id, action_type)
        conn.execute(query_string)
        db_connect.commit()
        db_connect.close()


    def post(self):
        tagtoaction = request.json
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        querystring = "delete from tagstoactions where tagid = {} and actiontype={}" \
            .format(tagtoaction["tagid"], tagtoaction["actiontype"])
        conn.execute(querystring)  # This line performs query and returns json result
        querystring = "INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES ('{}','{}','{}')" \
            .format(tagtoaction["tagid"], tagtoaction["actiontype"], tagtoaction["identifier"])
        conn.execute(querystring)  # This line performs query and returns json result
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok"})


class TagLog(Resource):

    def post(self):
        taglog = request.json
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()
        querystring = "INSERT INTO taglog (tagid, deviceid, start, stop, totaltimes) VALUES ('{}','{}','{}','{}',{})" \
            .format(taglog["tagid"], taglog["deviceid"], taglog["start"], taglog["stop"], taglog["totaltimes"])
        conn.execute(querystring)
        db_connect.commit()
        db_connect.close()
        return jsonify({"results": "ok"})


class TagLogQuery(Resource):

    def get(self, activity_type, activity_id, start, end):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()

        if activity_type == '1':
            query_string = "select sum(tl.totaltimes) from activities a " \
                           "join tagstoactions tta on a.activityid = tta.identifier and tta.actiontype = 1 " \
                           "join taglog tl on tl.tagid = tta.tagid where a.activityid = {} and " \
                           "tl.start >= '{}' and tl.stop <= '{}'" \
                .format(activity_id, start, end)

        query = conn.execute(query_string)
        objects_list = []
        for row in query:
            d = collections.OrderedDict()
            d['duration'] = row[0]
            if row[0] is None:
                d['duration'] = 0
            else:
                d['duration'] = row[0]

            objects_list.append(d)
        if len(objects_list) == 0:
            return {'duration': 0}
        db_connect.close()
        return objects_list[0]


class Label(Resource):

    def get(self, activity_id):
        db_connect = sqlite3.connect('droptime.db')
        conn = db_connect.cursor()

        query_string = "select label from activitiestolabels where activityid = '{}'" \
            .format(activity_id)

        query = conn.execute(query_string)
        objects_list = []
        for row in query:
            objects_list.append(row[0])
        db_connect.close()
        return objects_list


api.add_resource(LastSeenTag, '/lastseentag')  # Route_1
api.add_resource(TagsToActionsList, '/tagstoactions')  # Route_1
api.add_resource(TagsToActions,     '/tagstoactions', '/tagstoactions/<action_type>/<string:tag_id>', '/tagstoactions/<action_type>/<string:tag_id>/<string:device_id>')  # Route_1
api.add_resource(UsersList, '/users')  # Route_1UsersUpdate
api.add_resource(Users, '/users/<user_id>')  # Route_1
api.add_resource(Devices, '/devices')  # Route_1
api.add_resource(Tag, '/tag', '/tag/<string:tag_id>')
api.add_resource(Tags, '/tags/<string:user_id>', '/tags')  # Route_1
api.add_resource(Activities, '/activities', '/activities/<activity_id>')  # Route_1
api.add_resource(ActivitiesList, '/activities')  # Route_1
api.add_resource(Reminders, '/reminders', '/reminders/<string:user_id>', '/reminders/delete/<string:reminder_id>')  # Route_1
# api.add_resource(CurrentReminders, '/reminders/current/<current_time>')  # Route_1
api.add_resource(TagLog, '/taglog')  # Route_1
api.add_resource(TagLogQuery, '/taglog/<activity_type>/<activity_id>/start/<start>/end/<end>')  # Route_1
api.add_resource(Label, '/label/<activity_id>')  # Route_1

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        file = "debug_config.json"
    else:
        file = "configuration.json"

    configuration = Configuration(file)
    url = configuration.get_value("tag_api", "self_url")
    print("Url is {}".format(url))
    app.run(host=url, port=5002)
