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

    def get_activities(self):
        url = self.base_url + '/activities'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=my_headers)
        return r.json()

    def get_tracking(self):
        url = self.base_url + '/tracking'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=my_headers)
        return r.json()

    def stop_tracking(self, activity_id, stop_time):
        url = self.base_url + '/tracking/' + activity_id + '/stop'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        body = {"stoppedAt": stop_time}
        r = requests.post(url, headers=my_headers, json=body)
        return r.json()

    def start_tracking(self, activity_id, start_time):
        url = self.base_url + '/tracking/' + activity_id + '/start'
        my_headers = {'Authorization': 'Bearer ' + self.token}
        body = {"startedAt": start_time, "note": {"text": None, "tags": [], "mentions": []}}
        r = requests.post(url, headers=my_headers, json=body)
        return r.json()


p1 = TimularApi("NDcwMDBfYzU5MTUwMDQ2OWU4NDA4OWExZjFlMTZlNDhlNjFlMDM=", "NDJkNDY1MjZhMDk5NDAyZTg2YjNkNWIyNDVmYmFiYjc=")

print(p1.api_key)
print(p1.api_secret)
print(p1.token)

currentDT = datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
year = currentDT.year
month = currentDT.month
day = currentDT.day
hour = currentDT.hour
minute = currentDT.minute
second = currentDT.second
#stopTime = "%s-%d-%sT%s:%s:%s.678" % (year, month, day, hour, minute, second)
stopTime = currentDT.strftime("%Y-%m-%dT%H:%M:%S.000")
currentDT = datetime.datetime.utcnow()
year = currentDT.year
month = currentDT.month
day = currentDT.day
hour = currentDT.hour
minute = currentDT.minute
second = currentDT.second
#startTime = "%s-%d-%sT%s:%s:%s.678" % (year, month, day, hour, minute, second)
startTime = currentDT.strftime("%Y-%m-%dT%H:%M:%S.000")
print (startTime)
print(p1.get_activities())
print(p1.stop_tracking('369008', stopTime))
print(p1.start_tracking('369007', startTime))
print(p1.get_tracking())
