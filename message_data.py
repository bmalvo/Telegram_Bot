import datetime


class ReminderData:

    def __init__(self, message, time):
        self.message = message
        self.time = datetime.datetime.strptime(time, "%d/%m/%y %H: %M")

    def __repr__(self):
        return "Message: {0}; At Time: {1}".format(self.message, self.time.strftime("%d/%m%Y %H: %M"))