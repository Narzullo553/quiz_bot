from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
class IsPrivate(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        return msg.chat.type == types.ChatType.PRIVATE
