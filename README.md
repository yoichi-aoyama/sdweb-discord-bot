# sdweb-discord-bot

## Prerequisite

Please run [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) with the `--api` parameter before starting the bot.

e.g.
```bash
export COMMANDLINE_ARGS="--xformers --api"
```

## Run bot

1. Install dependencies
    ```bash
    $ pipenv install
    ```
1. Create `.env` file.
    ```.env
    GUILD_ID=<Your channel ID>
    DISCORD_BOT_TOKEN=<Your bot token>
    ```
1. Run bot
    ```bash
    $ pipenv run python discord_bot.py
    ```
