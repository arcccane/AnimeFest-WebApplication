class DisplayNames:
    countid= 0
    def __init__(self,image_location, dname , caption):
        DisplayNames.countid += 1
        self.__nameid = DisplayNames.countid
        self.__image_location = image_location
        self.__dname =dname
        self.__caption = caption

    def get_nameid(self):
        return self.__nameid

    def get_image_location(self):
        return self.__image_location

    def get_dname(self):
        return self.__dname

    def get_caption(self):
        return self.__caption

    def set_nameid(self, nameid):
        self.__nameid = nameid

    def set_image_location(self, image_location):
        self.__image_location = image_location

    def set_dname(self, dname):
        self.__dname = dname

    def set_caption(self, caption):
        self.__caption = caption
