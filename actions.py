class Actions:

    def __init__(self, timeular, my_logger):
        self.action_list = [timeular]
        self.logger = my_logger

    def execute(self, tag_id):
        self.logger.log("execute " + str(tag_id))
        for action in self.action_list:
            self.logger.log("action " + str(tag_id))
            if action.is_actionable(tag_id):
                self.logger.log("about to execute action " + str(tag_id))
                action.execute(tag_id)

