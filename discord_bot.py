import os
import uuid
from base64 import b64decode
from io import BytesIO

import discord
from discord import app_commands
from dotenv import load_dotenv
from PIL import Image, PngImagePlugin

from sdweb_api_handler import SDWebAPIHandler


load_dotenv()
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GUILD_ID = os.environ.get("GUILD_ID")
MY_GUILD = discord.Object(id=GUILD_ID)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} ({client.user.id})")


@client.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}")


@client.tree.command()
@app_commands.describe(
    prompt="image prompt",
)
async def txt2img(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(ephemeral=False)

    sd = SDWebAPIHandler()
    response = await sd.txt2img(prompt=prompt)
    generated_images = []
    for img in response["images"]:
        image = Image.open(BytesIO(b64decode(img)))
        pnginfo = PngImagePlugin.PngInfo()
        png_info_response = await sd.png_info(img)
        info_text = png_info_response.get("info")
        pnginfo.add_text("parameters", info_text)
        tmp_filename = f"{uuid.uuid4()}.png"
        generated_images.append(tmp_filename)
        image.save(tmp_filename, pnginfo=pnginfo)

    files = [discord.File(path, filename=path) for path in generated_images]
    for img in generated_images:
        os.remove(img)

    embed = discord.Embed(color=discord.Color.green())
    embed.set_image(url=f"attachment://{files[0].filename}")
    embed.add_field(name="Prompt", value=f"{prompt}")
    await interaction.followup.send(files=files, embed=embed)


client.run(DISCORD_BOT_TOKEN)
