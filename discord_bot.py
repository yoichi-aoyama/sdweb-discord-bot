import os
import uuid

from base64 import b64decode
from io import BytesIO

import discord

from PIL import Image, PngImagePlugin
from discord.ext import commands

from sdweb_api_handler import SDWebAPIHandler


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
sd = SDWebAPIHandler()


@bot.event
async def on_ready():
    print("Logged in")


@bot.command()
async def t2i(ctx, *, arg):
    generated_images = []
    prompt = arg
    for img in sd.txt2img(prompt)["images"]:
        image = Image.open(BytesIO(b64decode(img)))
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", sd.png_info(img).get("info"))
        tmp_filename = f"{uuid.uuid4()}.png"
        generated_images.append(tmp_filename)
        image.save(tmp_filename, pnginfo=pnginfo)

    payload = []
    for img in generated_images:
        with open(img, "rb") as f:
            payload.append(discord.File(f))
        os.remove(img)
    await ctx.send(f"Generate: {prompt}", files=payload)
