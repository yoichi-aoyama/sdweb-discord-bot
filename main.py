import os

from dotenv import load_dotenv
from discord_bot import bot


if __name__ == "__main__":
    load_dotenv(".env")
    token = os.environ.get("DISCORD_BOT_TOKEN")
    bot.run(token)
