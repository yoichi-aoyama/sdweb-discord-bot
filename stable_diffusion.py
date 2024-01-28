import json

from base64 import b64decode
from io import BytesIO
from logging import getLogger, INFO
from urllib.parse import urljoin

import requests

from PIL import Image, PngImagePlugin


class StableDiffusion:
    def __init__(self):
        self.base_url = "http://127.0.0.1:7860/"
        self.headers = {"Content-type": "application/json"}

    def queue_status(self):
        endpoint = "/queue/status"
        url = urljoin(self.base_url, endpoint)
        params = {}
        req = requests.get(url, headers=self.headers, params=params)
        return json.loads(req.text)

    def txt2img(self, prompt, negative_prompt="EasyNegative2", steps=20):
        endpoint = "/sdapi/v1/txt2img"
        url = urljoin(self.base_url, endpoint)
        params = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
        }
        req = requests.post(url, json=params)
        return json.loads(req.text)

    def png_info(self, image):
        endpoint = "/sdapi/v1/png-info"
        url = urljoin(self.base_url, endpoint)
        params = {"image": f"data:image/png;base64,{image}"}
        req = requests.post(url, json=params)
        return json.loads(req.text)


if __name__ == "__main__":
    logger = getLogger(__name__)
    logger.setLevel(INFO)

    sd = StableDiffusion()
    prompt = input("prompt:")

    for img in sd.txt2img(prompt)["images"]:
        image = Image.open(BytesIO(b64decode(img)))
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", sd.png_info(img).get("info"))
        image.save("output.png", pnginfo=pnginfo)
