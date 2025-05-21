import requests
import json
from config import OLLAMA_URL, OLLAMA_URL_VISION, MODEL_NAME, VISION_MODEL_NAME
from typing import Union
from pathlib import Path
from utils.image import resize_image

def get_ollama_response(messages: list) -> str:
    print(messages)
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "messages": messages
    }, stream=False)

    reply = ""
    for line in response.iter_lines():
        if line:
            data = line.decode("utf-8").removeprefix("data: ").strip()
            if data and data != "[DONE]":
                reply_chunk = json.loads(data).get("message", {}).get("content", "")
                reply += reply_chunk
    return reply

def analyze_image_with_llava(image_path: Union[str, Path], prompt: str = "What is in this picture?") -> str:
    image_path = Path(image_path)
    encoded_image = resize_image(image_path)

    response = requests.post(OLLAMA_URL_VISION, json={
        "model": VISION_MODEL_NAME,
        "prompt": prompt,
        "images": [encoded_image],
        "stream": False
    })

    if response.ok:
        return response.json().get("response", "").strip()
    else:
        return f"Error: {response.status_code} – {response.text}"

