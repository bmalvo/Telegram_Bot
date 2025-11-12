from telegram import Update, KeyboardButton, ReplyKeyboardMarkup 
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes, 
                          ConversationHandler, MessageHandler, filters, Updater,
                          CallbackContext)
from token_bot import EXACT_TOKEN_TYPES
from memory_datasourse import MemoryDataSourse

ENTER_MESSAGE, ENTER_TIME = 'range(2)', 'ee'
dataSource = MemoryDataSourse()


def add_reminder_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Please enter a message of the reminder:')
    return ENTER_MESSAGE


def enter_message_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Please enter a time when bot should remind:')
    context.user_data['message.text'] = update.message.text
    return ENTER_TIME


def enter_time_handler(update: Update, context: CallbackContext):
    message_text = context.user_data["message_text"]
    time = update.message.text
    message_data = dataSource.add_reminder(update.message.chat_id, message_text, time)
    update.message.reply_text("your reminder: " + message_data.__repr__())
    return ConversationHandler.END

conv_handler = ConversationHandler( 
    entry_points=[MessageHandler(filters.regex(ADD_REMINDER_TEXT), add_reminder_handler)]
    states = {
        ENTER_MESSAGE = [(MessageHandler(filters.all, enter_message_handler))],
        ENTER_TIME = [MessageHandler(filters.all, enter_time_handler)],
        fallbacks= []
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
    keyboard = [[KeyboardButton(ADD_REMINDER_TEXT)]]
    return ReplyKeyboardMarkup(keyboard)

updater = Updater(EXACT_TOKEN_TYPES, use_context= True)
updater.dispatcher.add_handler(CommandHandler('start', start_handler))
updater.dispatcher.add_handler(conv_handler)
 
app = ApplicationBuilder().token(EXACT_TOKEN_TYPES).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()
