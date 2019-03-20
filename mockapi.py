class MockApi:

    def __init__(self):
        print("init")

    def get_activities(self):
        print("get_activities")
        return "{}"


    def get_tracking(self):
        print("get_tracking")
        return "314"


    def stop_tracking(self, activity_id, stop_time=None):
        print("stop_tracking " + str(activity_id) + " " + str(stop_time))
        return {}


    def start_tracking(self, activity_id, start_time=None):
        print("start_tracking " + str(activity_id) + " " + str(start_time))
        return {}
