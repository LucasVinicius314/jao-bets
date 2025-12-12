import os
import discord
from discord.ext import commands
from events.voice_events import VoiceEvents
from database.mongo import MongoDB
from commands.bet.bet_buttons import BetButtons

class JaoClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True

        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("Bot iniciando...")

        await self.load_extension("events.voice_events")
        await self.load_extension("commands.economy.points")
        await self.load_extension("commands.bet.create_bet")
        synced = await self.tree.sync()
        print(f"global synced: {len(synced)}")

    async def on_ready(self):
        print(f"Bot online como {self.user}")

        mongo = MongoDB()

        self.add_view(BetButtons(mongo))

        print("🟢 Views persistentes registradas!")

        await self.restore_bets()

        voice_events = self.get_cog("VoiceEvents")
        if voice_events:
            await voice_events.scan_existing_voice_members()

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Streaming(
                name="Apostas online 🃏😈",
                url="https://www.twitch.tv/fariazinhu"
            )
        )

    async def restore_bets(self):
        mongo = MongoDB()
        bets_collection = mongo.db.bets
        bet_channel_id = int(os.getenv("BET_CHANNEL_ID"))

        try:
            channel = await self.fetch_channel(bet_channel_id)
        except:
            print("❌ Não consegui buscar o canal de apostas.")
            return

        async for bet in bets_collection.find({"status": "open"}):
            msg_id = bet.get("message_id")

            try:
                await channel.fetch_message(int(msg_id))
                print(f"🔁 Aposta restaurada: {bet['bet_id']}")
            except:
                print(f"⚠️ Não consegui restaurar mensagem da aposta {bet['bet_id']}")
