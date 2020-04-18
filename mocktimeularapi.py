class MockTimeularApi:
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
        labels = self.tag_repository.get_activity_labels(activity_id)
        if start_time is None:
            start_time = TimularApi.get_utc_time()
        current_tracking = self.get_tracking(token)
        if current_tracking is not None:
            self.stop_tracking(token, current_tracking, TimularApi.get_utc_time(True))
        url = self.base_url + '/tracking/' + str(activity_id) + '/start'
        my_headers = {'Authorization': 'Bearer ' + token}
        text = ""
        tags = []
        start_tag = 0
        for tag in labels:
            text = text + tag
            t = {"indices": [start_tag, len(tag) + start_tag]}
            start_tag = len(text)
            tags.append(t)
        body = {"startedAt": start_time, "note": {"text": text, "tags": tags, "mentions": []}}
        print(body)
        r = requests.post(url, headers=my_headers, json=body)
        return r.json()

    def get_token(self, api_key, api_secret):
        url = self.base_url + '/developer/sign-in'
        body = '{"apiKey": "' + api_key + '","apiSecret": "' + api_secret + '"}'
        r = requests.post(url, data=body)
        token = r.json()["token"]
        return token
