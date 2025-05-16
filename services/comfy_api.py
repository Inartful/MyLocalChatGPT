import json
import uuid
import urllib.request
import urllib.parse
import random
import os
import websocket
from config import COMFYUI_SERVER, OUTPUT_DIR
from utils.image import compress_image

client_id = str(uuid.uuid4())

def load_base_prompt(workflow_file: str = "realistic_tg_workflow.json"):
    with open(workflow_file, "r") as f:
        return json.load(f)

def build_prompt(prompt_text: str, negative_prompt_text: str = "", seed: int = None, workflow_file: str = "realistic_tg_workflow.json"):
    base = load_base_prompt(workflow_file)

    if seed is None:
        seed = random.randint(0, 2**63 - 1)

    # ДЕЛИКАТНО добавляем текст к уже существующему
    if "6" in base:
        base["6"]["inputs"]["text"] += "" + prompt_text

    if "7" in base:
        base["7"]["inputs"]["text"] += "" + negative_prompt_text

    if "3" in base:
        base["3"]["inputs"]["seed"] = seed

    return base


def queue_prompt(prompt_dict):
    payload = {
        "prompt": prompt_dict,
        "client_id": client_id
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{COMFYUI_SERVER}/prompt", data=data)
    with urllib.request.urlopen(req) as response:
        raw = response.read()
        return json.loads(raw)["prompt_id"]

def get_images_from_disk(prompt_dict):

    prompt_id = queue_prompt(prompt_dict)

    ws = websocket.WebSocket()
    ws.connect(f"ws://127.0.0.1:8188/ws?clientId={client_id}")

    while True:
        out = ws.recv()
        if isinstance(out, str):
            msg = json.loads(out)

            # Ожидаем именно завершения prompt'а — node == None
            if msg['type'] == 'executing':
                data = msg['data']
                if data.get('node') is None and data.get('prompt_id') == prompt_id:
                    break
    ws.close()

   
    # 📥 Получаем историю
    with urllib.request.urlopen(f"{COMFYUI_SERVER}/history/{prompt_id}") as response:
        history = json.load(response)

    if prompt_id not in history:
        raise RuntimeError(f"Prompt ID {prompt_id} not found in history")

    prompt_data = history[prompt_id]

    # 📤 Получаем изображение
    output_images = []
    for node_id, node_data in prompt_data.get("outputs", {}).items():
        for image in node_data.get("images", []):
            filename = image["filename"]
            subfolder = image["subfolder"]
            type_ = image["type"]

            params = urllib.parse.urlencode({
                "filename": filename,
                "subfolder": subfolder,
                "type": type_
            })
            
            image_path = os.path.join(OUTPUT_DIR, filename)

            with open(image_path, "rb") as f:
                output_images.append(f.read())
    
    compressed = []
    for img_bytes in output_images:
        compress = compress_image(img_bytes)
        compressed.append(compress)

    return compressed