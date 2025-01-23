from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from aiogram.types import Message, Poll, PollAnswer

class IsGroup(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        return msg.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)



class IsAdmin_group(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        try:
            member = await msg.bot.get_chat_member(msg.chat.id, msg.from_user.id)
            return member.is_chat_admin()
        except:
            return False


class IsAdmin_group_call(BoundFilter):
    async def check(self, call: types.CallbackQuery) -> bool:
        try:
            member = await call.bot.get_chat_member(call.message.chat.id, call.from_user.id)
            return member.is_chat_admin()
        except:
            return False


class IsPrivateChatFilter(BoundFilter):
    """
    Poll yoki PollAnswer shaxsiy chatga tegishliligini tekshirish uchun filter.
    """

    async def check(self, obj):
        # PollAnswer uchun user mavjud bo'lsa, chat turi shaxsiy bo'ladi.
        if isinstance(obj, PollAnswer):
            return obj.user is not None  # PollAnswer faqat shaxsiy chatda keladi

        # Message yoki Poll uchun shaxsiy chatni tekshiradi
        if isinstance(obj, (Message, Poll)):
            return obj.chat.type == "private"

        return False
