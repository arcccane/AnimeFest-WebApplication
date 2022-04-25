class Event:
    count_id = 0

    def __init__(self, title, date, starttime, endtime, url):
        Event.count_id += 1
        self.__event_id = Event.count_id
        self.__title = title
        self.__date = date
        self.__starttime = starttime
        self.__endtime = endtime
        self.__url = url

    def get_event_id(self):
        return self.__event_id

    def get_title(self):
        return self.__title

    def get_date(self):
        return self.__date

    def get_starttime(self):
        return self.__starttime

    def get_endtime(self):
        return self.__endtime

    def get_url(self):
        return self.__url

    def set_event_id(self, event_id):
        self.__event_id = event_id

    def set_title(self, title):
        self.__title = title

    def set_date(self, date):
        self.__date = date

    def set_starttime(self, starttime):
        self.__starttime = starttime

    def set_endtime(self, endtime):
        self.__endtime = endtime

    def set_url(self, url):
        self.__url = url
