import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient

# Load API credentials from .env
load_dotenv()

API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_NAME = 'threat_intel_agent'

print("🚀 Starting Telegram Authentication Process...")
print("⚠️ IMPORTANT: When prompted, enter the BURNER PHONE NUMBER (with country code, e.g., +1...)")

try:
    # Initialize client. The terminal will pause here for the phone number and code.
    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        me = client.get_me()
        print("\n✅ Authentication successful!")
        print(f"🕵️ Agent logged in as: {me.first_name} (ID: {me.id})")
        print("📁 Session file 'threat_intel_agent.session' has been generated securely.")
except Exception as e:
    print(f"\n❌ Error during authentication: {e}")