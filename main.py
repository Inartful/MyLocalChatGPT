#bot.py

from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from handlers import image, chat, bot, vision

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    for handler in vision.get_handlers():
        app.add_handler(handler)

    for handler in bot.get_handlers():
        app.add_handler(handler)

    for handler in chat.get_handlers():
        app.add_handler(handler)

    for handler in image.get_handlers():
        app.add_handler(handler)

    app.run_polling()

if __name__ == "__main__":
    main()
