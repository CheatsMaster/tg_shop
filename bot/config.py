import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]
    
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # WebApp
    WEBAPP_URL = os.getenv("WEBAPP_URL", "https://crash-shop.vercel.app")
    
    # Backblaze B2
    B2_KEY_ID = os.getenv("B2_KEY_ID")
    B2_APPLICATION_KEY = os.getenv("B2_APPLICATION_KEY")
    B2_BUCKET_NAME = os.getenv("B2_BUCKET_NAME")