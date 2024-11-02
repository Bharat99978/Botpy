import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import threading
import time

# Replace with your own token
TOKEN = '7228147192:AAEg1GtZGTGSr_uag1BMi2V6hwytNBBYb8o'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

elapsed_seconds = 0
stopwatch_thread = None
stopwatch_running = False

def start(update: Update, context: CallbackContext) -> None:
    global stopwatch_running, elapsed_seconds, stopwatch_thread
    
    if stopwatch_running:
        update.message.reply_text("Stopwatch is already running.")
        return

    update.message.reply_text("Stopwatch started! Type /stop to stop it.")
    
    elapsed_seconds = 0
    stopwatch_running = True

    # Start the stopwatch in a separate thread
    def run_stopwatch():
        global elapsed_seconds
        while stopwatch_running:
            time.sleep(1)
            elapsed_seconds += 1
            hours = elapsed_seconds // 3600
            minutes = (elapsed_seconds % 3600) // 60
            seconds = elapsed_seconds % 60
            formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Elapsed time: {formatted_time}")

    stopwatch_thread = threading.Thread(target=run_stopwatch)
    stopwatch_thread.start()

def stop(update: Update, context: CallbackContext) -> None:
    global stopwatch_running, elapsed_seconds, stopwatch_thread
    
    if not stopwatch_running:
        update.message.reply_text("Stopwatch is not running.")
        return

    stopwatch_running = False
    stopwatch_thread.join()  # Wait for the thread to finish
    hours = elapsed_seconds // 3600
    minutes = (elapsed_seconds % 3600) // 60
    seconds = elapsed_seconds % 60
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    update.message.reply_text(f"Stopwatch stopped! Final time: {formatted_time}")

    # Reset elapsed time
    elapsed_seconds = 0

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))

    # Start polling for updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
