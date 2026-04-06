"""from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()

async def get_db():
    conn = await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    return conn
"""
# app/database.py
from dotenv import load_dotenv
import asyncpg
from app.config import settings

load_dotenv()

async def get_db():
    conn = await asyncpg.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
    )
    return conn


