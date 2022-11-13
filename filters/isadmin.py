from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdminFilter(BaseFilter):
    user_id: Union[int | list]

    async def __call__(self, msg: Message):
        if isinstance(self.user_id, int):
            return msg.from_user.id == self.user_id
        else:
            return msg.from_user.id in self.user_id
