import logging


class Actions:

    def __init__(self, *actions):
        self.action_list = list(actions)

    def execute(self, tag_id):
        logging.debug("execute " + str(tag_id))
        action_return_type = {"ActionReturnType": "Unidentified"}
        for action in self.action_list:
            logging.debug("action " + str(tag_id))
            result = action.execute(tag_id)
            if "ActionReturnType" in result:
                action_return_type = result
        return action_return_type

    def poll(self, tag_id):
        logging.debug("poll " + str(tag_id))
        result_list = []
        for action in self.action_list:
            result = action.poll(tag_id)
            result_list.append(result)
        return result_list


if __name__ == "__main__":
    from mockledcontroller import MockLedController
    from mockaction import MockAction
    actions = Actions(MockLedController(), MockAction())
    actions.execute(314)
