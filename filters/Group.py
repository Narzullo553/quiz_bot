from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

class IsGroup(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        return msg.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)
