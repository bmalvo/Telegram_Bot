from message_data import ReminderData


class MemoryDataSourse:

    def __init__(self):
        self.reminders = dict()

    def add_reminder(self, chat_id, message, time):
        message_data = ReminderData(message, time)
        self.reminders[chat_id] = message_data
        return message_data
