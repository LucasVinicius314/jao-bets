from datetime import datetime
import discord

class BetButtons(discord.ui.View):
    def __init__(self, mongo):
        super().__init__(timeout=None)
        self.mongo = mongo

    @discord.ui.button(label="Apostar 1", style=discord.ButtonStyle.success, custom_id="bet_1")
    async def bet_1(self, interaction, button):
        await self.process_bet(interaction, 1)

    @discord.ui.button(label="Apostar 5", style=discord.ButtonStyle.primary, custom_id="bet_5")
    async def bet_5(self, interaction, button):
        await self.process_bet(interaction, 5)

    @discord.ui.button(label="Apostar 10", style=discord.ButtonStyle.danger, custom_id="bet_10")
    async def bet_10(self, interaction, button):
        await self.process_bet(interaction, 10)

    async def get_real_bet_id(self, interaction: discord.Interaction):
        bets_collection = self.mongo.db.bets
        msg_id = str(interaction.message.id)

        bet = await bets_collection.find_one({"message_id": msg_id})
        if not bet:
            return None
        
        return bet["bet_id"]

    async def process_bet(self, interaction: discord.Interaction, amount: int):

        bet_id = await self.get_real_bet_id(interaction)
        if not bet_id:
            return await interaction.response.send_message(
                "⚠️ Não consegui vincular esta aposta ao banco.",
                ephemeral=True
            )

        user_id = str(interaction.user.id)
        points_collection = self.mongo.db.points
        bets_collection = self.mongo.db.users_bets

        user_data = await points_collection.find_one({"user_id": user_id})

        if not user_data:
            await points_collection.insert_one({
                "user_id": user_id,
                "user_name": str(interaction.user),
                "points": 0
            })
            user_data = {"points": 0}

        current_points = user_data.get("points", 0)

        if current_points < amount:
            return await interaction.response.send_message(
                f"❌ Saldo insuficiente. Saldo: **{current_points}**",
                ephemeral=True
            )

        await points_collection.update_one(
            {"user_id": user_id},
            {"$inc": {"points": -amount}}
        )

        await interaction.response.send_message(
            f"🔔 Aposta registrada!",
            ephemeral=True
        )

        existing_bet = await bets_collection.find_one({
            "bet_id": bet_id,
            "user_id": user_id
        })

        if existing_bet:
            await bets_collection.update_one(
                {"bet_id": bet_id, "user_id": user_id},
                {"$inc": {"amount": amount}}
            )
        else:
            await bets_collection.insert_one({
                "bet_id": bet_id,
                "user_id": user_id,
                "user_name": str(interaction.user),
                "amount": amount,
                "timestamp": datetime.utcnow()
            })
