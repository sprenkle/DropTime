class Actions:

    def __init__(self, my_logger, *actions):
        self.action_list = list(actions)
        self.logger = my_logger

    def execute(self, tag_id):
        self.logger.log("execute " + str(tag_id))
        for action in self.action_list:
            self.logger.log("action " + str(tag_id))
            action.execute(tag_id)

