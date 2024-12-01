import asyncio
from urllib.parse import urljoin

import aiohttp


class SDWebAPIHandler:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/"

    async def _make_get_request(self, endpoint, params):
        url = urljoin(self.base_url, endpoint)
        timeout = aiohttp.ClientTimeout(total=36000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    async def _make_post_request(self, endpoint, params):
        url = urljoin(self.base_url, endpoint)
        timeout = aiohttp.ClientTimeout(total=36000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=params) as response:
                return await response.json()

    async def txt2img(
        self,
        prompt,
        negative_prompt="EasyNegative2",
        sampler_name="DPM++ 2M Karras",
        batch_size=1,
        steps=20,
        cfg_scale=7.0,
        width=512,
        height=512,
        restore_faces=False,
        enable_hr=False,  # FIXME: If True, an error occurs
        hr_scale=1.5,
        lcm_model_id="stabilityai/sd-turbo",
        openvino_lcm_model_id="rupeshs/sd-turbo-openvino",
        hr_upscaler="SwinIR 4x",
    ):
        endpoint = "/api/generate"
        params = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "sampler_name": sampler_name,
            "batch_size": batch_size,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "image_width": width,
            "image_height": height,
            "restore_faces": restore_faces,
            #"enable_hr": enable_hr,
            #"hr_scale": hr_scale,
            #"hr_upscaler": hr_upscaler,
            "lcm_model_id": lcm_model_id,
            "openvino_lcm_model_id": openvino_lcm_model_id,
        }
        return await self._make_post_request(endpoint, params)


    async def txt2imglora(
        self,
        prompt,
        negative_prompt="EasyNegative2",
        sampler_name="DPM++ 2M Karras",
        batch_size=1,
        steps=20,
        cfg_scale=7.0,
        width=512,
        height=512,
        restore_faces=False,
        enable_hr=False,  # FIXME: If True, an error occurs
        hr_scale=1.5,
        lcm_model_id="SimianLuo/LCM_Dreamshaper_v7",
        #openvino_lcm_model_id="rupeshs/sd-turbo-openvino",
        hr_upscaler="SwinIR 4x",
    ):
        endpoint = "/api/generate"
        params = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "sampler_name": sampler_name,
            "batch_size": batch_size,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "image_width": width,
            "image_height": height,
            "restore_faces": restore_faces,
            #"enable_hr": enable_hr,
            #"hr_scale": hr_scale,
            #"hr_upscaler": hr_upscaler,
            "lcm_model_id": lcm_model_id,
            "lcm_lora": { 'base_model_id': 'Lykon/dreamshaper-8',
              'lcm_lora_id': 'latent-consistency/lcm-lora-sdv1-5'},
            "use_openvino": True,
        }
        return await self._make_post_request(endpoint, params)
    async def png_info(self, image):
        endpoint = "/sdapi/v1/png-info"
        params = {"image": f"data:image/png;base64,{image}"}
        return await self._make_post_request(endpoint, params)

    async def sd_models(self):
        endpoint = "/api/models"
        params = {}
        return await self._make_get_request(endpoint, params)

    async def sd_vae(self):
        endpoint = "/sdapi/v1/sd-vae"
        params = {}
        return await self._make_get_request(endpoint, params)

    async def get_config(self):
        endpoint = "/api/config"
        params = {}
        return await self._make_get_request(endpoint, params)

    async def set_config(self, params):
        endpoint = "/sdapi/v1/options"
        return await self._make_post_request(endpoint, params)
    async def info(self, params):
        endpoint = "/api/info"
        return await self._make_post_request(endpoint, params)


async def main():
    sd = SDWebAPIHandler()
    res = await sd.sd_vae()
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
