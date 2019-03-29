class MockAction:
    def __init__(self):
        pass

    def get_id(self):
        return 314

    def poll(self, tag_id):
        pass

    def execute(self, tag_id):
        return {"has_progress": True}
