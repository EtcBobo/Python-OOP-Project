class Registration:

    def __init__(self,user,password,minPrice,maxPrice,foodType,email):
        self.__user = user
        self.__password = password
        self.__minPrice = minPrice
        self.__maxPrice = maxPrice
        self.__foodType = foodType
        self.__email = email

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_minPrice(self):
        return self.__minPrice

    def get_foodType(self):
        return self.__foodType

    def get_maxPrice(self):
        return self.__maxPrice

    def get_email(self):
        return self.__email
