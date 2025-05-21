# handlers/vision

import os
from uuid import uuid4
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler, filters
from services.ollama_client import analyze_image_with_llava
from config import TEMP_IMAGE_DIR
from state.chat_memory import chat_histories
from utils.chat_history import append_to_history

os.makedirs(TEMP_IMAGE_DIR, exist_ok=True)

async def handle_user_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("📷 Пожалуйста, отправьте изображение.")
        return

    chat_id = update.effective_chat.id
    photo = update.message.photo[-1]
    file = await photo.get_file()

    file_name = f"{uuid4().hex}.jpg"
    file_path = os.path.join(TEMP_IMAGE_DIR, file_name)

    try:
        await file.download_to_drive(custom_path=file_path)
        await update.message.reply_text("🧐 Мико-чан смотрит на картинку...~")

        description = analyze_image_with_llava(file_path)
        response = f"🖼️ Мико-чан видит:\n\n{description or '...ничего? Как странно!'}"

        append_to_history(chat_id, "user", "<image>")
        append_to_history(chat_id, "assistant", response)

        await update.message.reply_text(response)
    except Exception as e:
        error_msg = f"😵 Что-то пошло не так: {e}"
        append_to_history(chat_id, "user", "<image>")
        append_to_history(chat_id, "assistant", error_msg)
        await update.message.reply_text(error_msg)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def get_handlers():
    return [
        MessageHandler(filters.PHOTO, handle_user_image),
    ]
