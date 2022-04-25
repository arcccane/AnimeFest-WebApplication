class Enquiry:
    count_id = 0

    def __init__(self, name, email, topic, enquirys):
        Enquiry.count_id += 1
        self.__enquiry_id = Enquiry.count_id
        self.__name = name
        self.__email = email
        self.__topic = topic
        self.__enquirys = enquirys

    def get_enquiry_id(self):
        return self.__enquiry_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_topic(self):
        return self.__topic

    def get_enquirys(self):
        return self.__enquirys

    def set_enquiry_id(self, enquiry_id):
        self.__enquiry_id = enquiry_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_topic(self, topic):
        self.__topic = topic

    def set_enquirys(self, enquirys):
        self.__enquirys = enquirys
