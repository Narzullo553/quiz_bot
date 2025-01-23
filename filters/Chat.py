from aiogram import types
from aiogram.types import PollAnswer, Message, ChatType
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, obj: Message or PollAnswer) -> bool:

        if isinstance(obj, Message):
            return obj.chat.type == ChatType.PRIVATE
        elif isinstance(obj, PollAnswer):
            user_id = obj.user.id
            chat = await obj.bot.get_chat(user_id)
            return chat.type == ChatType.PRIVATE
        return False