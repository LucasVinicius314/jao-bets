import datetime
from zoneinfo import ZoneInfo
from discord.ext import commands
from database.mongo import MongoDB

UTC3 = ZoneInfo("America/Sao_Paulo")

class VoiceEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo = MongoDB()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        collection = self.mongo.db.points
        user_id = str(member.id)

        # viadinho entra na call
        if before.channel is None and after.channel is not None:
            now = datetime.datetime.now(UTC3)
            print(f"{member} entrou na call - {now.strftime('%Y-%m-%d %H:%M:%S')}")

            await collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {"last_join": datetime.datetime.utcnow()},
                    "$setOnInsert": {"user_name": str(member)}
                },
                upsert=True
            )

        # viadinho sai da call
        if before.channel is not None and after.channel is None:
            now = datetime.datetime.now(UTC3)
            print(f"{member} saiu da call - {now.strftime('%Y-%m-%d %H:%M:%S')}")

            user_data = await collection.find_one({"user_id": user_id})
            if not user_data or "last_join" not in user_data:
                return

            joined_at = user_data["last_join"]
            now_utc = datetime.datetime.utcnow()

            minutes = int((now_utc - joined_at).total_seconds() // 60)
            points_to_add = minutes

            await collection.update_one(
                {"user_id": user_id},
                {
                    "$inc": {"points": points_to_add},
                    "$unset": {"last_join": ""}
                }
            )
            print(f"{member} ganhou {points_to_add} pontos por {minutes} minutos em call.")

async def setup(bot):
    await bot.add_cog(VoiceEvents(bot))
