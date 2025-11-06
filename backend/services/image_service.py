from PIL import Image
from io import BytesIO

class ImageService:
    def __init__(self):
        self.size = 512, 512
    
    def resize_image(self, image_bytes: bytes) -> bytes:
        with Image.open(BytesIO(image_bytes)) as im:
            im.thumbnail(self.size)
            out = BytesIO()
            
            fmt = im.format if im.format else "PNG"
            im.save(out, format=fmt)
            out.seek(0)
            return out.read()
