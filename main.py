import asyncio
import logging

from bot import get_bot
from clients.chadprogress import ChadProgressClient
from config.config import Config
from dispatcher import dp
from handlers import start
from repo.sqlite.sqlite import ChadProgressDB


async def main():
    logging.basicConfig(level=logging.INFO)
    cfg = Config()
    bot = get_bot(cfg.TELEGRAM_BOT_TOKEN)

    cp_client = ChadProgressClient(cfg.CHADPROGRESS_API_URL)
    cp_db = ChadProgressDB(cfg.STORAGE_PATH)
    await cp_db.init_db()

    dp["cp_client"] = cp_client
    dp["cp_db"] = cp_db

    include_routers(dp)
    
    await dp.start_polling(bot)

def include_routers(dp):
    dp.include_router(
        start.rt
    )

if __name__ == "__main__":
    asyncio.run(main())