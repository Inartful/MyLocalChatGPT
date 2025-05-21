#handlers/chat.py

from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from state.chat_memory import chat_histories
from state.image_state import user_states
from services.ollama_client import get_ollama_response
from utils.texts import COMMANDS_TEXT
from utils.chat_history import append_to_history


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMANDS_TEXT["start"])

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMANDS_TEXT["help"])

async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_histories.pop(chat_id, None)
    user_states.pop(user_id, None)
    await update.message.reply_text("🧹 Всё очищено. Можно начинать заново!")

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    msg = update.message.text

    history = append_to_history(chat_id, "user", msg)
    reply = get_ollama_response(history)
    append_to_history(chat_id, "assistant", reply)

    await update.message.reply_text(reply or "🤷 Модель ничего не ответила.")


def get_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("reset", reset_all),
        CommandHandler("help", help_command),
    ]
