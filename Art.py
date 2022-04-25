class Art:
    countid= 0


    def __init__(self,image_location,firstname, lastname, email, phone, age, gender, sname):
        Art.countid += 1
        self.__userid = Art.countid
        self.__image_location=image_location
        self.__firstname = firstname
        self.__lastname = lastname
        self.__email = email
        self.__phone = phone
        self.__age = age
        self.__gender = gender
        self.__sname = sname

    def get_userid(self):
        return self.__userid

    def get_image_location(self):
        return self.__image_location

    def get_firstname(self):
        return self.__firstname

    def get_lastname(self):
        return self.__lastname

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_age(self):
        return self.__age

    def get_gender(self):
        return self.__gender

    def get_sname(self):
        return self.__sname

    def set_userid(self, userid):
        self.__userid = userid

    def set_image_location(self,image_location):
        self.__image_location=image_location

    def set_firstname(self, firstname):
        self.__firstname = firstname

    def set_lastname(self, lastname):
        self.__lastname = lastname

    def set_email(self, email):
        self.__email = email

    def set_phone(self, phone):
        self.__phone = phone

    def set_age(self, age):
        self.__age = age

    def set_gender(self, gender):
        self.__gender = gender

    def set_sname(self, sname):
        self.__sname = sname
