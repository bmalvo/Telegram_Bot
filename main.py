from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from token_bot import EXACT_TOKEN_TYPES


async def hello(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}', 
        reply_markup=add_reminder_button)
    # await update.message.reply_text(
    #     'hello, creator!', reply_markup=add_reminder_button())

def add_reminder_button():
    keyboard = [[KeyboardButton('add a reminder ⏰')]]
    return ReplyKeyboardMarkup(keyboard)


app = ApplicationBuilder().token(EXACT_TOKEN_TYPES).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()
