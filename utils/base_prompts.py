from datetime import datetime

def get_system_prompt():
    now = datetime.now().strftime("%d.%m.%Y")
    return {
    "role": "assistant",
    "content": (
        f"The time now is: {now}. "
        )
    }

