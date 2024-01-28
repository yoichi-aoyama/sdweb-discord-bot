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
async def imagine(ctx, *args):
    prompt = "".join(args)
    for img in sd.txt2img(prompt)["images"]:
        image = Image.open(BytesIO(b64decode(img)))
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", sd.png_info(img).get("info"))
        image.save("output.png", pnginfo=pnginfo)
    with open("output.png", "rb") as f:
        image = discord.File(f)
        await ctx.send(f"Generate: {prompt}", file=image)
