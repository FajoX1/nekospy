from aiogram import types
from aiogram.types import FSInputFile

from nekospy import config, bot, db, redis

import os
import git
import asyncio

async def get_git_info():
    repo = git.Repo(search_parent_directories=True)
    git_dir = os.path.join(os.getcwd(), ".git")
    if not os.path.isdir(git_dir):
        raise FileNotFoundError("Not a git repository")
        
    with open(os.path.join(git_dir, "HEAD"), "r") as head_file:
        ref_line = head_file.readline().strip()
        if ref_line.startswith("ref:"):
            branch = ref_line.split("/")[-1]
            ref_path = os.path.join(git_dir, *ref_line.split(" ")[1].split("/"))
        else:
            branch = None
            ref_path = None
    
    repo.git.fetch()

    if ref_path and os.path.isfile(ref_path):
        with open(ref_path, "r") as ref_file:
            last_commit = ref_file.readline().strip()
    elif ref_line:
        last_commit = ref_line.strip()
    else:
        last_commit = None

    last_commit_short = last_commit[:7]

    return {
        "branch": branch,
        "last_commit": last_commit,
        "last_commit_short": last_commit_short
    }

async def set_message(message: types.Message):
    if message.from_user.id == config.ADMIN_ID:
        return

    user = await db.user.get(message.from_user.id)
    if not user:
        topic = await bot.create_forum_topic(
            chat_id=config.LOG_CHAT_ID,
            name=message.from_user.full_name
        )
        await db.user.add_user(message.from_user.id, topic.message_thread_id)

    await redis.set(
        f"{message.chat.id}:{message.message_id}",
        message.model_dump_json(),
        ex=config.REDIS_EXPIRE_DAYS * 60 * 60 * 24,
    )


async def send_media(bot, chat_id, user, media_type, file_id, message_thread_id):
    file_path = f"{file_id}.{media_type}"
    await bot.download(file_id, destination=file_path)

    if media_type == "jpg":
        media = FSInputFile(path=file_path)
        await bot.send_photo(
            chat_id=chat_id, message_thread_id=user.topic_id, photo=media
        )
    elif media_type == "mp4":
        media = FSInputFile(path=file_path)
        if "video_note" in file_id:
            await bot.send_video_note(
                chat_id=chat_id, message_thread_id=user.topic_id, video_note=media
            )
        else:
            await bot.send_video(
                chat_id=chat_id, message_thread_id=user.topic_id, video=media
            )
    elif media_type == "ogg":
        media = FSInputFile(path=file_path)
        await bot.send_voice(
            chat_id=chat_id, message_thread_id=user.topic_id, voice=media
        )

    await asyncio.sleep(1.2)
    os.remove(file_path)
