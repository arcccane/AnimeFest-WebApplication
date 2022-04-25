class Feedback:
    count_id = 0

    def __init__(self, ratings , remarks):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__ratings = ratings
        self.__remarks = remarks

    def get_feedback_id(self):
        return self.__feedback_id

    def get_ratings(self):
        return self.__ratings

    def get_remarks(self):
        return self.__remarks

    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id


    def set_ratings(self, ratings):
        self.__ratings = ratings

    def set_remarks(self, remarks):
        self.__remarks = remarks