class Cart:
    count = 0

    def __init__(self):
        Cart.count += 1
        self.__cart_id = Cart.count
        self.__user_id = 0
        self.__product_list = []

    def get_cart_id(self):
        return self.__cart_id

    def get_product_list(self):
        return self.__product_list

    def get_user_id(self):
        return self.__user_id

    def add_product_id(self, product_id):
        self.__product_list.append(product_id)

    def set_user_id(self, user_id):
        self.__user_id = user_id
