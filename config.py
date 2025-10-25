import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROK_API_KEY")
BASE_URL = os.getenv("GROK_BASE_URL")