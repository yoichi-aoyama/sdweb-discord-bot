from base64 import b64decode
from io import BytesIO

from PIL import Image, PngImagePlugin

from sdweb_api_handler import SDWebAPIHandler

if __name__ == "__main__":
    sd = SDWebAPIHandler()
    prompt = input("prompt:")

    for img in sd.txt2img(prompt)["images"]:
        image = Image.open(BytesIO(b64decode(img)))
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", sd.png_info(img).get("info"))
        image.save("output.png", pnginfo=pnginfo)
