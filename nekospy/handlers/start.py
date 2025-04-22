from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart

from nekospy import config, utils
from nekospy.filters.is_admin import IsAdminFilter

router = Router()
# router.message.filter(
#    IsAdminFilter(is_admin=True)
# )

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    git_info = await utils.get_git_info()

    await message.answer_animation(
        animation="https://i.gifer.com/A9H.gif",
        caption=f"""<b>🤖 NekoSpy 2.0 <a href="https://github.com/fajox1/nekospy/blob/{git_info['last_commit']}">#{git_info['last_commit_short']}</a>

👤 Admin: <a href="tg://user?id={config.ADMIN_ID}">open</a>

🧑‍💻 Developer: @fajox
🐈‍⬛ GitHub: <a href="https://github.com/fajox1/nekospy">open</a></b>"""
    )