import requests
import datetime


class TimularApi:
    # ApiKey = NDcwMDBfYzU5MTUwMDQ2OWU4NDA4OWExZjFlMTZlNDhlNjFlMDM=
    # ApiSecret = NDJkNDY1MjZhMDk5NDAyZTg2YjNkNWIyNDVmYmFiYjc=
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api.timeular.com/api/v2'
        url = self.base_url + '/developer/sign-in'
        body = '{"apiKey": "' + self.api_key + '","apiSecret": "' + self.api_secret + '"}'
        r = requests.post(url, data=body)
        self.token = r.json()['token']

    @staticmethod
    def get_utc_time(minus=False):
        current_dt = datetime.datetime.utcnow()
        if minus:
            current_dt = current_dt - datetime.timedelta(seconds=1)
        current_time = current_dt.strftime("%Y-%m-%dT%H:%M:%S.000")
        return current_time

    def get_activities(self):
        url = self.base_url + '/activities'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=my_headers)
        return r.json()

    def get_tracking(self):
        url = self.base_url + '/tracking'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=my_headers)
        current_tracking = r.json()["currentTracking"];
        if current_tracking is None:
            return None
        return current_tracking["activity"]["id"]

    def stop_tracking(self, activity_id, stop_time=None):
        if stop_time is None:
            stop_time = TimularApi.get_utc_time()
        url = self.base_url + '/tracking/' + activity_id + '/stop'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        body = {"stoppedAt": stop_time}
        r = requests.post(url, headers=my_headers, json=body)
        return r.json()

    def start_tracking(self, activity_id, start_time=None):
        if start_time is None:
            start_time = TimularApi.get_utc_time()
        current_tracking = self.get_tracking()
        if current_tracking is not None:
            self.stop_tracking(current_tracking, TimularApi.get_utc_time(True))
        url = self.base_url + '/tracking/' + activity_id + '/start'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        body = {"startedAt": start_time, "note": {"text": None, "tags": [], "mentions": []}}
        r = requests.post(url, headers=my_headers, json=body)
        return r.json()


if __name__ == "__main__":
    p1 = TimularApi("NDcwMDBfYzU5MTUwMDQ2OWU4NDA4OWExZjFlMTZlNDhlNjFlMDM=", "NDJkNDY1MjZhMDk5NDAyZTg2YjNkNWIyNDVmYmFiYjc=")

    # print(p1.api_key)
    # print(p1.api_secret)
    # print(p1.token)

    #print (startTime)
    #print(p1.get_activities())
    #print(p1.stop_tracking('369007', TimularApi.get_utc_time()))
    #print(TimularApi.get_utc_time(True))
    #time = TimularApi.get_utc_time(True)
    print(p1.start_tracking('369007'))
    #print(p1.get_tracking())
