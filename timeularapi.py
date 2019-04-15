import requests
import datetime
from configuration import Configuration
from tagrepository import TagRepository
import logging
import json

# 2019-03-31T16:57:02.000


class TimularApi:
    def __init__(self, configuration, tag_repository):
        self.configuration = configuration
        self.base_url = self.configuration.get_value("timeular_api", "url")
        self.tag_repository = tag_repository;

    @staticmethod
    def get_utc_time(minus=False):
        current_dt = datetime.datetime.utcnow()
        if minus:
            current_dt = current_dt - datetime.timedelta(seconds=1)
        current_time = current_dt.strftime("%Y-%m-%dT%H:%M:%S.000")
        return current_time

    def get_activities(self, token):
        logging.info("TimularApi get_activities")
        url = self.base_url + '/activities'
        my_headers = {'Authorization': 'Bearer ' + token}
        r = requests.get(url, headers=my_headers)
        return r.json()

    def get_tracking(self, token):
        logging.info("TimularApi get_tracking")
        url = self.base_url + '/tracking'
        my_headers = {'Authorization': 'Bearer ' + token}
        r = requests.get(url, headers=my_headers)
        current_tracking = r.json()["currentTracking"];
        if current_tracking is None:
            return None
        return current_tracking["activity"]["id"]

    def stop_tracking(self, token, activity_id, stop_time=None):
        logging.info("TimularApi stop_tracking " + str(activity_id))
        if stop_time is None:
            stop_time = TimularApi.get_utc_time()
        url = self.base_url + '/tracking/' + str(activity_id) + '/stop'
        my_headers = {'Authorization': 'Bearer ' + token}
        body = {"stoppedAt": stop_time}
        r = requests.post(url, headers=my_headers, json=body)
        return r.json()

    def start_tracking(self, token, activity_id, start_time=None):
        logging.info("TimularApi start_tracking " + str(activity_id))
        labels = self.tag_repository.get_activity_labels(activity_id);
        if start_time is None:
            start_time = TimularApi.get_utc_time()
        current_tracking = self.get_tracking(token)
        if current_tracking is not None:
            self.stop_tracking(token, current_tracking, TimularApi.get_utc_time(True))
        url = self.base_url + '/tracking/' + str(activity_id) + '/start'
        my_headers = {'Authorization': 'Bearer ' + token}
        body = {"startedAt": start_time, "note": {"text": None, "tags": labels, "mentions": []}}
        print(body)
        r = requests.post(url, headers=my_headers, json=body)
        return r.json()

    def get_token(self, api_key, api_secret):
        url = self.base_url + '/developer/sign-in'
        body = '{"apiKey": "' + api_key + '","apiSecret": "' + api_secret + '"}'
        r = requests.post(url, data=body)
        token = r.json()["token"]
        return token


if __name__ == "__main__":
    file = "configuration.json"
    configuration = Configuration(file)
    p1 = TimularApi(configuration, TagRepository(configuration))
    #print(p1.get_token(1))

    # print(p1.api_key)
    # print(p1.api_secret)
    # print(p1.token)

    #print (startTime)
    #print(p1.get_activities())
    #print(p1.stop_tracking('369007', TimularApi.get_utc_time()))
    #print(TimularApi.get_utc_time(True))
    #time = TimularApi.get_utc_time(True)
    print(p1.get_token(1))
    #print(p1.get_tracking())
