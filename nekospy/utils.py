from aiogram import types

from nekospy import config, bot, db, redis

import os
import git

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
        ex=60*60*24*21,
    )