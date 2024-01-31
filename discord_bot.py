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
sd = SDWebAPIHandler()


@client.event
async def on_ready():
    print(f"Logged in as {client.user} ({client.user.id})")


@client.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}")


@client.tree.command()
async def get_config(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    response = await sd.get_config()
    embed = discord.Embed(color=discord.Color.green())
    embed.add_field(
        name="sd_model_checkpoint", value=response["sd_model_checkpoint"], inline=False
    )
    embed.add_field(name="sd_vae", value=response["sd_vae"], inline=False)
    await interaction.followup.send(embed=embed)


@client.tree.command()
async def get_models(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    response = await sd.sd_models()
    embed = discord.Embed(title="SD Models", color=discord.Color.green())
    for i, v in enumerate(response):
        embed.add_field(
            name=f"{i}:",
            value=v["title"],
            inline=False,
        )
    await interaction.followup.send(embed=embed)


@client.tree.command()
async def get_vae(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    response = await sd.sd_vae()
    embed = discord.Embed(title="SD VAE", color=discord.Color.green())
    for i, v in enumerate(response):
        embed.add_field(
            name=f"{i}:",
            value=v["model_name"],
            inline=False,
        )
    await interaction.followup.send(embed=embed)


@client.tree.command()
@app_commands.describe(
    model="model [hash]",
)
async def set_model(interaction: discord.Interaction, model: str):
    await interaction.response.defer(ephemeral=False)
    params = {"sd_model_checkpoint": model}
    response = await sd.set_config(params)
    embed = discord.Embed(title="Set Model", color=discord.Color.green())
    embed.add_field(
        name="Result",
        value=response,
        inline=False,
    )
    await interaction.followup.send(embed=embed)


@client.tree.command()
@app_commands.describe(
    vae="vae",
)
async def set_vae(interaction: discord.Interaction, vae: str):
    await interaction.response.defer(ephemeral=False)
    params = {"sd_vae": vae}
    response = await sd.set_config(params)
    embed = discord.Embed(title="Set VAE", color=discord.Color.green())
    embed.add_field(
        name="Result",
        value=response,
        inline=False,
    )
    await interaction.followup.send(embed=embed)


@client.tree.command()
@app_commands.describe(
    prompt="Prompt: Default (None)",
    negative_prompt="Negative Prompt: Default (EasyNegative2)",
    steps="Setps: Default (20)",
    cfg_scale="CFG Scale: Default (7.0)",
)
async def txt2img(
    interaction: discord.Interaction,
    prompt: str,
    negative_prompt: str = "EasyNegative2",
    steps: int = 20,
    cfg_scale: float = 7.0,
):
    await interaction.response.defer(ephemeral=False)

    response = await sd.txt2img(
        prompt=prompt,
        negative_prompt=negative_prompt,
        steps=steps,
        cfg_scale=cfg_scale,
    )
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
    embed.add_field(
        name="Options",
        value=f"""
        negative_prompt: {negative_prompt}
        steps: {steps}
        cfg_scale: {cfg_scale}
        """,
    )
    await interaction.followup.send(files=files, embed=embed)


client.run(DISCORD_BOT_TOKEN)
