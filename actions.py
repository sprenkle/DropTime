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

        # action_result = action_result_list["ActionReturnType"]
        #
        # # determine how to display the led
        # if self.reminder.has_reminders():
        #     pass
        #  #   self.process_reminders()
        # else:
        #     if card_id is None:
        #         self.led_controller.stop_progress()
        #         self.led_controller.clear()
        #         logging.info("returned Result list = {}".format(action_result))
        #     elif action_result == "NoDisplay":
        #         self.led_controller.show_non_result_display()
        #     elif action_result == "Unidentified":
        #         self.led_controller.show_non_action_tag()
        #     elif action_result == "Progress":
        #         goal_time = action_result_list["goal_total"]
        #         total_time = action_result_list["time_spent"]
        #         self.led_controller.start_progress(goal_time, total_time)

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
