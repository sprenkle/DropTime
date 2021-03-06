import datetime


class MockRfiReader:

    def __init__(self):
        self.arr = ['1110505110']
        self.last_event_time = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        self.last_event = None
        self.index = 0

    def read_tag(self):
        if self.last_event_time < datetime.datetime.utcnow() - datetime.timedelta(seconds=5):
            if self.index == len(self.arr):
                self.index = 0
            self.last_event = self.arr[self.index]
            self.last_event_time = datetime.datetime.utcnow()
            self.index = self.index + 1
        return self.last_event

    def stop(self):
        pass


if __name__ == "__main__":
    reader = MockRfiReader()
    start_time = datetime.datetime.utcnow()
    while start_time < datetime.datetime.utcnow() + datetime.timedelta(seconds=120):
        print(reader.read_tag())
