from PIL import Image
import io

def compress_image(img_bytes):
    img = Image.open(io.BytesIO(img_bytes))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)  # можно ещё меньше quality
    buf.seek(0)
    return buf