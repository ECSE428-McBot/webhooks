from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta

class MacBusService:

    # academic year starting and ending dates
    academicStart = date(2016, 9, 1)
    academicEnd = date(2017, 4, 28)

    # regular schedules
    regularDS = [time(hour=7, minute=20), time(hour=7, minute=30), time(hour=7, minute=45), time(hour=8, minute=30),
                 time(hour=9, minute=15), time(hour=10, minute=0), time(hour=10, minute=30), time(hour=10, minute=45),
                 time(hour=11, minute=30), time(hour=12, minute=15), time(hour=13, minute=0), time(hour=13, minute=15),
                 time(hour=13, minute=45), time(hour=14, minute=30), time(hour=15, minute=15), time(hour=16, minute=0),
                 time(hour=16, minute=15), time(hour=16, minute=45), time(hour=17, minute=45), time(hour=18, minute=15)]
    regularMS = [time(hour=7, minute=0), time(hour=7, minute=45), time(hour=8, minute=40), time(hour=9, minute=0),
                 time(hour=9, minute=15), time(hour=10, minute=0), time(hour=10, minute=45), time(hour=11, minute=30),
                 time(hour=11, minute=50), time(hour=12, minute=15), time(hour=13, minute=0), time(hour=13, minute=45),
                 time(hour=14, minute=30), time(hour=14, minute=45), time(hour=15, minute=15), time(hour=16, minute=0),
                 time(hour=16, minute=45), time(hour=17, minute=45), time(hour=18, minute=0), time(hour=18, minute=15)]

    # reading week starting and ending dates
    readingStart = date(2017, 2, 27)
    readingEnd = date(2017, 3, 3)

    # reading week schedules
    readingDS = [time(hour=7, minute=20), time(hour=8, minute=30), time(hour=10, minute=0), time(hour=11, minute=30),
                 time(hour=13, minute=0), time(hour=14, minute=30), time(hour=16, minute=45), time(hour=18, minute=15)]
    readingMS = [time(hour=7, minute=0), time(hour=8, minute=40), time(hour=10, minute=0), time(hour=11, minute=30),
                 time(hour=13, minute=0), time(hour=14, minute=30), time(hour=16, minute=45), time(hour=18, minute=15)]

    # summer schedules
    summerDS = [time(hour=8, minute=30), time(hour=17, minute=30)]
    summerMS = [time(hour=7, minute=30), time(hour=18, minute=30)]

    @staticmethod
    def getCurrentTime():
        return datetime.now().time()

    @staticmethod
    def getCurrentDate():
        return datetime.now().date()

    @staticmethod
    def searchSchedule(currentTime, schedule):

        for i in range(0, len(schedule), 1):

            if currentTime <= schedule[i]:
                return schedule[i].strftime("%H:%M")

        return None # no more bus today

    # Find the correct date in the semester.
    @staticmethod
    def locateDate(downtown, currentDate, currentTime):
        # Check if the date is in academic year.
        if MacBusService.academicStart <= currentDate <= MacBusService.academicEnd:
            # Check if the date is in reading week.
            if MacBusService.readingStart <= currentDate <= MacBusService.readingEnd:
                if downtown is True:
                    result = MacBusService.searchSchedule(currentTime, MacBusService.readingDS)  # downtown campus
                else:
                    result = MacBusService.searchSchedule(currentTime, MacBusService.readingMS)  # mac campus
            else:
                if downtown is True:
                    result = MacBusService.searchSchedule(currentTime, MacBusService.regularDS)  # downtown campus
                else:
                    result = MacBusService.searchSchedule(currentTime, MacBusService.regularMS)  # mac campus
        else:
            if downtown is True:
                result = MacBusService.searchSchedule(currentTime, MacBusService.summerDS)  # downtown campus
            else:
                result = MacBusService.searchSchedule(currentTime, MacBusService.summerMS)  # mac campus

        # Search for tomorrow's schedule if there is no more bus today.
        if result is None:
            result = "Tomorrow " + MacBusService.locateDate(downtown, currentDate + timedelta(days=1), time(hour=0, minute=0))

        return result

    def giveNextBus(user):
        # Verify user type.
        if user.user_type == 'student':
            currentDate = MacBusService.getCurrentDate()
            currentTime = MacBusService.getCurrentTime()

            return "Right now is " + currentTime.strftime("%H:%M") + ". Downtown: " + MacBusService.locateDate(True, currentDate, currentTime) + ", Macdonald: " + MacBusService.locateDate(False, currentDate, currentTime)
        else:
            return "This service is not open due to your user type."  # user type error
