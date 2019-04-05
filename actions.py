class Actions:

    def __init__(self, my_logger, *actions):
        self.action_list = list(actions)
        self.logger = my_logger

    def execute(self, tag_id):
        self.logger.log("execute " + str(tag_id))
        action_return_type = {"ActionReturnType": "Unidentified"}
        for action in self.action_list:
            self.logger.log("action " + str(tag_id))
            result = action.execute(tag_id)
            if "ActionReturnType" in result:
                action_return_type = result
        return action_return_type

    def poll(self, tag_id):
        self.logger.log("poll " + str(tag_id))
        result_list = []
        for action in self.action_list:
            result = action.poll(tag_id)
            result_list.append(result)
        return result_list


if __name__ == "__main__":
    from mockledcontroller import MockLedController
    from logger import Logger
    from mockaction import MockAction
    actions = Actions(MockLedController(), Logger(), MockAction())
    actions.execute(314)
