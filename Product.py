class Product:
    count_id = 0

    def __init__(self, product_name, product_description,price, promotion, company, category):
        Product.count_id += 1
        self.__product_id = Product.count_id
        self.__product_name = product_name
        self.__product_description = product_description
        self.__price = price
        self.__promotion = promotion
        self.__company = company
        self.__category = category

    def get_product_id(self):
        return self.__product_id

    def get_product_name(self):
        return self.__product_name

    def get_product_description(self):
        return self.__product_description

    def get_price(self):
        return self.__price

    def get_promotion(self):
        return self.__promotion

    def get_company(self):
        return self.__company

    def get_category(self):
        return self.__category

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_product_description(self, product_description):
        self.__product_description = product_description

    def set_price(self, price):
        self.__price = price

    def set_promotion(self, promotion):
        self.__promotion = promotion

    def set_company(self, company):
        self.__company = company

    def set_category(self, category):
        self.__category = category
