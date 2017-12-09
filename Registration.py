class Registration:

    def __init__(self,user,password,price,foodType):
        self.__user = user
        self.__password = password
        self.__price = price
        self.__foodType = foodType

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_price(self):
        return self.__price

    def get_foodType(self):
        return self.__foodType
