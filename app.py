
from aiogram import executor

from keyboards.inline.bosh_menu import create_quiz_menu
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import ADMINS

async def on_startup(dispatcher):
    try:
        await set_default_commands(dispatcher)
        try:
            db.create_table_users()
            db.create_savollar()
        except Exception as e:
            print(e)
        await on_startup_notify(dispatcher)
    except Exception as error:
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, f"{error}")
            except Exception as err:
                pass



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
