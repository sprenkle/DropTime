class Actions:

    def __init__(self, tag_repository, led_controller, my_logger, *actions):
        self.action_list = list(actions)
        self.logger = my_logger
        self.led_controller = led_controller
        self.tag_repository = tag_repository

    def execute(self, tag_id):
        self.logger.log("execute " + str(tag_id))
        for action in self.action_list:
            self.logger.log("action " + str(tag_id))
            result = action.execute(tag_id)
            if result is not None and "has_progress" in result:
                if result["has_progress"]:
                    print(result["has_progress"])
                    goal_time = result["goal_time"]
                    start_amount = result["total_amount_time"]
                    self.led_controller.start_progress(goal_time, start_amount)
                else:
                    self.led_controller.stop_progress()

    def poll(self, tag_id):
        self.logger.log("poll " + str(tag_id))
        for action in self.action_list:
            self.logger.log("action type:{}  tagid:{}".format(action.get_id(), str(tag_id)))
            result = action.execute(tag_id)

    def log_tag(self, tag_id, start, end):
        self.tag_repository.log_tag(tag_id, start, end)


if __name__ == "__main__":
    from mockledcontroller import MockLedController
    from logger import Logger
    from mockaction import MockAction
    actions = Actions(MockLedController(), Logger(), MockAction())
    actions.execute(314)
