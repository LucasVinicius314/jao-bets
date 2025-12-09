import discord
from discord.ext import commands

class JaoClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        print("Bot iniciando...")
        
    async def on_ready(self):
        print(f"Bot online como {self.user}")

        activity = discord.Streaming(
            name="Apostas online 🃏😈",
            url="https://www.twitch.tv/fariazinhu"
        )

        await self.change_presence(
            status=discord.Status.online,
            activity=activity
        )
    
    async def setup_hook(self):
        await self.load_extension("events.voice_events")
        await self.load_extension("commands.economy.points")
        synced = await self.tree.sync()
        print(f"global synced: {len(synced)}")

