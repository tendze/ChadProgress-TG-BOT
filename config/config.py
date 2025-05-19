import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.CHADPROGRESS_API_URL = os.getenv("CHADPROGRESS_API_URL")
        self.STORAGE_PATH = os.getenv("STORAGE_FILE_PATH")

        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env")
        if not self.CHADPROGRESS_API_URL:
            raise ValueError("Missing CHADPROGRESS_API_URL in .env")
        if not self.STORAGE_PATH:
            raise ValueError("Missing STORAGE_FILE_PATH in .env")
