class Actions:

    def __init__(self, timeular):
        self.action_list = [timeular]

    def execute(self, tag_id):
        for action in self.action_list:
            if action.is_actionable(tag_id):
                action.execute(tag_id)

