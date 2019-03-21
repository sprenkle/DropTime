import datetime


class MockRfiReader:

    def __init__(self):
        self.arr = ['231965344320', None, '438308258332', None]
        self.last_event_time = datetime.datetime.utcnow()
        self.last_event = None
        self.index = -1;

    def read_card(self):
        if self.last_event_time < datetime.datetime.utcnow() - datetime.timedelta(seconds=15):
            self.index = self.index + 1
            if self.index >= len(self.arr) - 1:
                self.index = 0
            self.last_event = self.arr[self.index]
            self.last_event_time = datetime.datetime.utcnow()
        return self.last_event


if __name__ == "__main__":
    reader = MockRfiReader()
    start_time = datetime.datetime.utcnow()
    while start_time < datetime.datetime.utcnow() + datetime.timedelta(seconds=120):
        print(reader.read_card())
