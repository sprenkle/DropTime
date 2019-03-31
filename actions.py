class Actions:

    def __init__(self, my_logger, *actions):
        self.action_list = list(actions)
        self.logger = my_logger

    def execute(self, tag_id):
        self.logger.log("execute " + str(tag_id))
        result_list = []
        for action in self.action_list:
            self.logger.log("action " + str(tag_id))
            result_list.append(action.execute(tag_id))
        return result_list

    def poll(self, tag_id):
        self.logger.log("poll " + str(tag_id))
        result_list = []
        for action in self.action_list:
            self.logger.log("action type:{}  tagid:{}".format(action.get_id(), str(tag_id)))
            result = action.execute(tag_id)
            result_list.append(result)
        return result_list




if __name__ == "__main__":
    from mockledcontroller import MockLedController
    from logger import Logger
    from mockaction import MockAction
    actions = Actions(MockLedController(), Logger(), MockAction())
    actions.execute(314)
