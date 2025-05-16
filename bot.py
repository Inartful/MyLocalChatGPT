from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from handlers import image, chat

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    for handler in chat.get_handlers():
        app.add_handler(handler)

    for handler in image.get_handlers():
        app.add_handler(handler)

    app.run_polling()

if __name__ == "__main__":
    main()
