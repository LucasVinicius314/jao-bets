from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDB:
    def __init__(self):
        uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB")

        if not uri:
            raise Exception("❌ MONGO_URI não encontrado no .env")
        if not db_name:
            raise Exception("❌ MONGO_DB não encontrado no .env")

        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
