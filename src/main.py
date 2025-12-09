import os
from dotenv import load_dotenv
from bot.client import JaoClient

load_dotenv()

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        print("ERRO: DISCORD_TOKEN não definido no .env")
        exit()

    client = JaoClient()
    client.run(token)
