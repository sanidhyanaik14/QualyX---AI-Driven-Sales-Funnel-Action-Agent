import asyncio
from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()

async def test_connection():
    try:
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 5432)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        print("✅ Connected to database successfully!")
        await conn.close()
        print("🔒 Connection closed.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

asyncio.run(test_connection())