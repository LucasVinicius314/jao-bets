from datetime import datetime
from dotenv import load_dotenv
import os
import uuid
import discord
from discord import app_commands
from discord.ext import commands
from database.mongo import MongoDB
from .bet_buttons import BetButtons

load_dotenv()

class CreateBetSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo = MongoDB()

    @app_commands.command(
        name="create_bet",
        description="Cria uma nova aposta."
    )
    async def create_bet(self, interaction: discord.Interaction, bet: str):
        perm_users = os.getenv("ADM_USERS_IDS")
        bet_channel_id = os.getenv("BET_CHANNEL_ID")
        collection = self.mongo.db.bets

        await interaction.response.defer(ephemeral=False)

        user_id = str(interaction.user.id)
        if perm_users and user_id not in perm_users.split(","):
            return await interaction.followup.send(
                embed=discord.Embed(
                    title="❌ Sem permissão",
                    color=discord.Color.red()
                )
            )

        bet_id = str(uuid.uuid4())
        channel = interaction.guild.get_channel(int(bet_channel_id))

        embed_channel_bet = discord.Embed(
            title="📢 Nova Aposta!",
            description=f"{bet}\n\nClique abaixo para apostar:",
            color=discord.Color.yellow()
        )

        view = BetButtons(self.mongo)
        msg = await channel.send(embed=embed_channel_bet, view=view)

        await collection.insert_one({
            "bet_id": bet_id,
            "creator_id": user_id,
            "bet_details": bet,
            "status": "open",
            "message_id": str(msg.id)
        })

        await interaction.followup.send(
            embed=discord.Embed(
                title="Aposta criada!",
                description=f"ID: `{bet_id}`",
                color=discord.Color.green()
            )
        )

async def setup(bot):
    await bot.add_cog(CreateBetSlash(bot))
