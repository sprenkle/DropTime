class CardRepository:

    def __init__(self):
        self.activity_dict = {231965344320: "369007", 438308258332: "369008", 25991398012: "369006"}

    def contains_id(self, tag_id):
        return tag_id in self.activity_dict

    def activity_id(self, tag_id):
        return self.activity_dict[tag_id]
