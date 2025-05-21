from PIL import Image
import io
import base64

def compress_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)  # можно ещё меньше quality
    buf.seek(0)
    return buf

def resize_image(image_path, max_size=(672, 672)) -> str:
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail(max_size, Image.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=75)
        buffer.seek(0) 
        return base64.b64encode(buffer.read()).decode("utf-8")