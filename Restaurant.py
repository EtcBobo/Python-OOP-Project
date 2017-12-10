class Restaurant:

    def __init__(self,name,description,location,price,foodType,openH,closingH,address,comment):
        self.__name = name
        self.__description = description
        self.__location = location
        self.__price = price
        self.__foodType = foodType
        self.__openH = openH
        self.__closingH = closingH
        self.__comment = comment
        self.__address = address

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_location(self):
        return self.__location

    def get_price(self):
        return self.__price

    def get_foodType(self):
        return self.__foodType

    def get_openH(self):
        return self.__openH

    def get_closingH(self):
        return self.__closingH

    def get_comment(self):
        return self.__comment

    def get_address(self):
        return self.__address