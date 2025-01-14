
from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import ADMINS

async def on_startup(dispatcher):
    try:
        await set_default_commands(dispatcher)
        await on_startup_notify(dispatcher)
    except Exception as error:
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, f"{error}")
            except Exception as err:
                pass



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
