import os
from dotenv import load_dotenv



load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN ValueError")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY ValueError")


if not POSTGRES_HOST:
    raise ValueError("POSTGRES_HOST ValueError")
if not POSTGRES_PORT:
    raise ValueError("POSTGRES_PORT ValueError")
if not POSTGRES_USER:
    raise ValueError("POSTGRES_USER ValueError")
if not POSTGRES_PASSWORD:
    raise ValueError("POSTGRES_PASSWORD ValueError")
if not POSTGRES_DB:
    raise ValueError("POSTGRES_DB ValueError")


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
