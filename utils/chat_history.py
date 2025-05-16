from state.chat_memory import chat_histories
from utils.base_prompts import get_system_prompt
from config import MAX_HISTORY_LENGTH

def get_or_init_history(chat_id):
    return chat_histories.get(chat_id, [get_system_prompt()])

def append_to_history(chat_id, role, content):
    history = get_or_init_history(chat_id)
    history.append({"role": role, "content": content})
    chat_histories[chat_id] = [history[0]] + history[1:][-MAX_HISTORY_LENGTH:]
    return history
