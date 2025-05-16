import requests
import json
from config import OLLAMA_URL, MODEL_NAME

def get_ollama_response(messages: list) -> str:
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": messages
    }, stream=True)

    reply = ""
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8").removeprefix("data: ").strip()
            if data and data != "[DONE]":
                reply_chunk = json.loads(data).get("message", {}).get("content", "")
                reply += reply_chunk
    return reply
