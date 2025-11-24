from telegram import Update, KeyboardButton, ReplyKeyboardMarkup 
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, 
                          ConversationHandler, MessageHandler, filters, Updater,
                          CallbackContext)
from token_bot import EXACT_TOKEN_TYPES, DATABASE_URL
# from memory_datasourse import MemoryDataSourse
import threading
import time
import datetime

INTERVAL = 30

ENTER_MESSAGE, ENTER_TIME = 'range(2)', 'ee'
dataSource = DATABASE_URL


def add_reminder_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Please enter a message of the reminder:')
    return ENTER_MESSAGE


def enter_message_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Please enter a time when bot should remind:')
    context.user_data['message.text'] = update.message.text
    return ENTER_TIME


def enter_time_handler(update: Update, context: CallbackContext):
    message_text = context.user_data["message_text"]
    time = datetime.datetime.strptime(update.message.text, "%d/%m/%y %H: %M")
    message_data = dataSource.create_reminder(update.message.chat_id, message_text, time)
    update.message.reply_text("your reminder: " + message_data.__repr__())
    return ConversationHandler.END

def start_check_reminders_task():
    thread = threading.Thread(target=check_reminders, args=())
    thread.daemon = True
    thread.start()

def check_reminders():
    while True:
        for reminder_data in dataSource.get_all_reminders():
            # reminder_data = dataSource.reminders[chat_id]
            if reminder_data.should_be_fired():
                # reminder_data.fire()
                dataSource.fire_reminder(reminder_data.reminder_id)
                updater.bot.send_message(reminder_data.chat_id, reminder_data.message)
        time.sleep(INTERVAL)


conv_handler = ConversationHandler( 
    entry_points=[MessageHandler(filters.Regex(
        'Add a reminder '), add_reminder_handler)],
    states = {
        ENTER_MESSAGE: [(MessageHandler(filters.ALL, enter_message_handler))],
        ENTER_TIME: [MessageHandler(filters.ALL, enter_time_handler)],
        # fallbacks= []
    },
    fallbacks = []
)

async def hello(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}', 
        reply_markup=add_reminder_button)
    # await update.message.reply_text(
    #     'hello, creator!', reply_markup=add_reminder_button())

def add_reminder_button():
    keyboard = [[KeyboardButton('Add a reminder ')]]
    return ReplyKeyboardMarkup(keyboard)

def start_handler(update, context):
    update.message.reply_text('Hello, creator!', reply_markup=add_reminder_button())

updater = Updater(EXACT_TOKEN_TYPES, update_queue=True)
updater.dispatcher.add_handler(CommandHandler('start', start_handler))
updater.dispatcher.add_handler(conv_handler)
 
app = ApplicationBuilder().token(EXACT_TOKEN_TYPES).build()

app.add_handler(CommandHandler("hello", hello))
dataSource.create_tables()
app.run_polling()
start_check_reminders_task()
