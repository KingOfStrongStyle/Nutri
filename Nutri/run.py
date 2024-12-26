import asyncio
import os

from app.user import user

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    bot.my_admins_list = []
    db = Dispatcher()
    db.include_router(user)
    await db.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    
    

