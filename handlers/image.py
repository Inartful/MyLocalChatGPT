from telegram.ext import CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from state.image_state import user_states, STATE_WAITING_MODEL, STATE_WAITING_POSITIVE, STATE_WAITING_NEGATIVE
from services.comfy_api import build_prompt, get_images_from_disk
from utils.chat_history import append_to_history
from config import MAX_HISTORY_LENGTH

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {
        "state": STATE_WAITING_MODEL,
        "model": None,
        "positive_prompt": "",
        "negative_prompt": ""
    }
    await update.message.reply_text("Выбери тип изображения:\n1. Реализм\n2. Иллюстрация")

async def handle_image_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    message = update.message.text.strip().lower()

    if user_id not in user_states:
        return

    user_data = user_states[user_id]
    state = user_data["state"]

    try:
        if state == STATE_WAITING_MODEL:
            if message in ["1", "2"]:
                user_data["model"] = "realistic_tg_workflow.json" if message == "1" else "anime_tg_workflow.json"
                user_data["state"] = STATE_WAITING_POSITIVE
                await update.message.reply_text("Отлично! Теперь введи позитивный промпт на английском, через запятую ✨")

                mage_type = "Realism" if message == "1" else "Illustration"
                append_to_history(chat_id, "user", f"Selected image type: {image_type}")
            else:
                await update.message.reply_text("Пожалуйста, выбери: `1` или `2`")
        
        elif state == STATE_WAITING_POSITIVE:
            user_data["positive_prompt"] = message
            user_data["state"] = STATE_WAITING_NEGATIVE
            await update.message.reply_text("Теперь введи негативный промпт на английском ❌")
    

            ahappend_to_history(chat_id, "user", f"Positive prompt: {message}")

        elif state == STATE_WAITING_NEGATIVE:
            user_data["negative_prompt"] = message
            await update.message.reply_text("Генерирую... 🧠")

            append_to_history(chat_id, "user", f"Negative prompt: {message}")

            prompt = build_prompt(
                prompt_text=user_data["positive_prompt"],
                negative_prompt_text=user_data["negative_prompt"],
                workflow_file=user_data["model"]
            )
            images = get_images_from_disk(prompt)

            if not images:
                await update.message.reply_text("Не удалось получить изображение 😢 Попробуй позже или проверь настройки.")
                append_to_history(chat_id, "assistant", "Failed to generate image.")
            else:
                for img in images:
                    await update.message.reply_photo(photo=img)
                    append_to_history(chat_id, "assistant", "Generated image")

            chat_histories[chat_id] = [history[0]] + history[1:][-MAX_HISTORY_LENGTH:]
            user_states.pop(user_id, None)
            await update.message.reply_text("Готово! Отправь /generate, чтобы попробовать снова 🚀")

    except Exception as e:
        append_to_history(chat_id, "assistant", "Failed to generate image.")
        user_states.pop(user_id, None)
        await update.message.reply_text("Упс, что-то пошло не так при генерации изображения. Попробуй позже.")
        print(f"Error for user {user_id}: {e}")

def get_handlers():
    return [
        CommandHandler("generate", generate_image)
    ]
