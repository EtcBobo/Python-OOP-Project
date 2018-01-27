class Events:

    def __init__(self,eventName,eventDescription,eventLocation,eventAddress,startDate,endDate,startTime,endTime, startTimeMin, endTimeMin, ticket, people):
        self.__eventName = eventName
        self.__eventDescription = eventDescription
        self.__eventLocation = eventLocation
        self.__eventAddress = eventAddress
        self.__startDate = startDate
        self.__endDate = endDate
        self.__startTime = startTime
        self.__endTime = endTime
        self.__startTimeMin = startTimeMin
        self.__endTimeMin = endTimeMin
        self.__ticket = ticket
        self.__people = 0

    def get_eventName(self):
        return self.__eventName

    def get_eventDescription(self):
        return self.__eventDescription

    def get_eventLocation(self):
        return self.__eventLocation

    def get_eventAddress(self):
        return self.__eventAddress

    def get_startDate(self):
        return self.__startDate

    def get_endDate(self):
        return self.__endDate

    def get_ticket(self):
        return self.__ticket

    def get_people(self):
        return self.__people

    def get_startTime(self):
        return self.__startTime

    def get_endTime(self):
        return self.__endTime

    def get_startTimeMin(self):
        return self.__startTimeMin

    def get_endTimeMin(self):
        return self.__endTimeMin
