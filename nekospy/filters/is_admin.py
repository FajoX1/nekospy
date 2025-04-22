from aiogram.filters import BaseFilter
from aiogram.types import Message

from nekospy import config

class IsAdminFilter(BaseFilter):
    """
    Filter that checks for admin rights existence
    """
    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

        self.admin = config.ADMIN_ID

    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == self.admin:
            return True == self.is_admin
        return False == self.is_admin