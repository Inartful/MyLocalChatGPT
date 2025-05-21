# handlers/bot.py

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from handlers.image import handle_image_prompt
from handlers.chat import handle_chat
from state.image_state import user_states

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in user_states:
        await handle_image_prompt(update, context)
    else:
        await handle_chat(update, context)

def get_handlers():
    return [
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
    ]
