import os
from dotenv import load_dotenv
import sys

load_dotenv()

DASHBOARD_URL = os.getenv("DASHBOARD_URL")
API_KEY = os.getenv("API_KEY")
ORG_ID = os.getenv("ORG_ID")

if not DASHBOARD_URL or not API_KEY or not ORG_ID:
    print("❌ Missing required environment variables in .env")
    sys.exit(1)
