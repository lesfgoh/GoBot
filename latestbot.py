from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from requests import *

import logging


addresses = dict()





API_KEY = '1739361402:AAHjOM-pKQRuA25ZB2b5iAIkXA391CVCftE'



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
# Best practice would be to replace context with an underscore,
# since context is an unused local variable.


def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text('Hi! I\'m a bot run by Les F Goh. Click /info to learn more.', disable_notification = True)

def add_address(chat_ID, location):
    addresses[chat_ID] = location.lower()

def notify(location):
    for i in addresses:
        if location.lower() in addresses[i]:
            print(i)

def submit(update: Update, context: CallbackContext) -> None:
    location = context.args[0].lower()
    for i in addresses:
        if location in addresses[i]:
            update.message.reply_text(i, disable_notification = True)
            context.bot.send_message(chat_id=str(i), text='A ride has opened up to ' + location + ' !')
    
    
def delete(chat_ID):
    del(addresses[chat_ID])

def init(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(context.args)
    if context.args:
        add_address(update.effective_user.id, context.args[0])
    else:
        update.message.reply_text("Please provide locations which you live near, for example: /sethome CCK. Spaces are not allowed!", disable_notification = True)

def show(update:Update, context: CallbackContext) -> None:
    update.message.reply_text("Show function is being called.")
    update.message.reply_text(addresses)
    
def showme(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Showme function is being called.")
    update.message.reply_text(addresses[update.effective_chat.id])

def info (update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Please enter /sethome <General Area> e.g /sethome CCK . For now, the bot doesn't accept spaces: Input YewTee instead of Yew Tee. Any input will be changed to lowercase letters! \nYou can either message me directly, or in the GoBek group. For more questions, please contact my creator at @importr on.", disable_notification = True)

def report(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("This function isn't enabled yet.")

def alarm(update: Update, context: CallbackContext) -> None:
    job = context.job
    context.bot.send_message(job.context, text='Beep!')
    
##def messageHandler(update: Update, context: CallbackContext):
##    update.message.reply_text('Sorry, this message isn\'t recognised.')
    
def trial(update:Update, context: CallbackContext):
    pass

def sethome(update: Update, context: CallbackContext):
    if context.args:
        place = context.args[0]
        chat_id, user_id = update.effective_chat.id, update.effective_user.id
        admin_bot = Bot(API_KEY)
        admin_bot.promote_chat_member(-1001591604870, user_id, False, False, False, False, True)
        admin_bot.set_chat_administrator_custom_title(-1001591604870, user_id, place.lower().replace(" ",""))
        update.message.reply_text("Done!", disable_notification= True)
        pass
    else:
        update.message.reply_text("Please provide a general location you live near, for example: /sethome CCK. Spaces are not allowed!", disable_notification = True)

def match(update:Update, context: CallbackContext):
    if context.args:
        pass
    else:
        pass

def feedback(update: Update, context: CallbackContext):
    update.message.reply_text("Please directly message @importr, my creator, to suggest new functionalities or even just to criticise their grammar!", disable_notification = True)


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Initialise list of locations
    locations = ["yewtee", "sengkang", "woodlands", "angmokio", "lakeside"]
    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("report", report))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("alarm", alarm))
    dispatcher.add_handler(CommandHandler("sethome", sethome))
    dispatcher.add_handler(CommandHandler("match", match))
    dispatcher.add_handler(CommandHandler("feedback", feedback))
    
    # Only these commands are being tested now. The rest are not relevant, and are for different purposes.
    
    dispatcher.add_handler(CommandHandler("show", show))
    dispatcher.add_handler(CommandHandler("showme", showme))
    dispatcher.add_handler(CommandHandler("init", init))
    dispatcher.add_handler(CommandHandler("submit", submit))


##    dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()




