import json

from base64 import b64decode
from io import BytesIO
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

    def txt2img(
        self,
        prompt,
        negative_prompt="EasyNegative2",
        sampler_name="DPM++ 2M Karras",
        batch_size=1,
        steps=20,
        cfg_scale=7,
        width=512,
        height=512,
        restore_faces=False,
        enable_hr=False,  # FIXME: If True, an error occurs
        hr_scale=1.5,
        hr_upscaler="SwinIR 4x",
    ):
        endpoint = "/sdapi/v1/txt2img"
        url = urljoin(self.base_url, endpoint)
        params = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "sampler_name": sampler_name,
            "batch_size": batch_size,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            "restore_faces": restore_faces,
            "enable_hr": enable_hr,
            "hr_scale": hr_scale,
            "hr_upscaler": hr_upscaler,
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
    sd = StableDiffusion()
    prompt = input("prompt:")

    for img in sd.txt2img(prompt)["images"]:
        image = Image.open(BytesIO(b64decode(img)))
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", sd.png_info(img).get("info"))
        image.save("output.png", pnginfo=pnginfo)
