import discord
from discord import app_commands
from discord.ext import commands
from database.mongo import MongoDB

class PointsSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo = MongoDB()

    @app_commands.command(
        name="pontos",
        description="Mostra quantos pontos você ou outro usuário tem."
    )
    @app_commands.describe(user="Mencione um usuário (opcional)")
    async def pontos(
        self,
        interaction: discord.Interaction,
        user: discord.User | None = None
    ):
        await interaction.response.defer(ephemeral=False)

        target = user or interaction.user

        user_id = str(target.id)
        collection = self.mongo.db.points

        user_data = await collection.find_one({"user_id": user_id})

        if not user_data:
            embed = discord.Embed(
                title="Nenhum registro encontrado",
                description=f"{target.mention} ainda não possui pontos registrados.",
                color=discord.Color.red()
            )
            return await interaction.followup.send(embed=embed)

        points = user_data.get("points", 0)
        name = target.mention

        embed = discord.Embed(
            title="💰 Dindin do gado",
            color=discord.Color.green()
        )
        embed.add_field(name="👤 Gado", value=name, inline=False)
        embed.add_field(name="⭐ Dindin", value=f"**{points}**", inline=False)
        embed.set_thumbnail(url=target.avatar)
        embed.set_footer(text=f"Solicitado por {interaction.user}")

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PointsSlash(bot))
