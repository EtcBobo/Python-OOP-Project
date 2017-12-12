class Registration:

    def __init__(self,user,password,price,foodType,email):
        self.__user = user
        self.__password = password
        self.__price = price
        self.__foodType = foodType
        self.__email = email

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_price(self):
        return self.__price

    def get_foodType(self):
        return self.__foodType

    # def set_email(self, email):
    #     self.__email = email

    def get_email(self):
        return self.__email
