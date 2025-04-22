from aiogram import types
from aiogram import Router

from nekospy import dp, bot, redis, config, db, utils
from nekospy.keyboards.main import edited_message_kb
from nekospy.utils import send_media

import asyncio

router = Router()

@dp.business_message()
async def message(message: types.Message):
    if message.reply_to_message and message.from_user.id == config.ADMIN_ID:
        model_dump = await redis.get(f"{message.chat.id}:{message.reply_to_message.message_id}")

        if model_dump:
            return

        user = await db.user.get(message.reply_to_message.from_user.id)

        await bot.send_message(
            chat_id=config.LOG_CHAT_ID,
            text="<b>🔥 Self destructed message:</b>",
            message_thread_id=user.topic_id,
        )

        if message.reply_to_message.photo:
            await send_media(bot, config.LOG_CHAT_ID, user, 'jpg', message.reply_to_message.photo[-1].file_id, user.topic_id)
        elif message.reply_to_message.video:
            await send_media(bot, config.LOG_CHAT_ID, user, 'mp4', message.reply_to_message.video.file_id, user.topic_id)
        elif message.reply_to_message.voice:
            await send_media(bot, config.LOG_CHAT_ID, user, 'ogg', message.reply_to_message.voice.file_id, user.topic_id)
        elif message.reply_to_message.video_note:
            await send_media(bot, config.LOG_CHAT_ID, user, 'mp4', message.reply_to_message.video_note.file_id, user.topic_id)

    await utils.set_message(message)

@dp.edited_business_message()
async def edited_message(message: types.Message):
    model_dump = await redis.get(f"{message.chat.id}:{message.message_id}")
    await utils.set_message(message)

    if not model_dump:
        return

    original_message = types.Message.model_validate_json(model_dump)
    if not original_message.from_user:
        return
    
    user = await db.user.get(original_message.from_user.id)
    
    await bot.send_message(
        chat_id=config.LOG_CHAT_ID,
        message_thread_id=user.topic_id,
        text="<b>✏️ Edit message, old message:</b>",
    )
    await original_message.send_copy(
        chat_id=config.LOG_CHAT_ID,
        message_thread_id=user.topic_id,
        reply_markup=await edited_message_kb(
            message_link=f"tg://openmessage?user_id={original_message.from_user.id}&message_id={original_message.message_id}"
        ),
    ).as_(bot)

@dp.deleted_business_messages()
async def deleted_message(business_messages: types.BusinessMessagesDeleted):
    pipe = redis.pipeline()
    for message_id in business_messages.message_ids:
        pipe.get(f"{business_messages.chat.id}:{message_id}")
    messages_data = await pipe.execute()

    keys_to_delete = []
    for message_id, model_dump in zip(business_messages.message_ids, messages_data):
        if not model_dump:
            continue

        original_message = types.Message.model_validate_json(model_dump)
        if not original_message.from_user:
            continue

        user = await db.user.get(original_message.from_user.id)

        await bot.send_message(
            chat_id=config.LOG_CHAT_ID,
            message_thread_id=user.topic_id,
            text="<b>🗑 Deleted message:</b>",
        )
        await original_message.send_copy(
            chat_id=config.LOG_CHAT_ID,
            message_thread_id=user.topic_id,
        ).as_(bot)

        await asyncio.sleep(1.2)

        keys_to_delete.append(f"{business_messages.chat.id}:{message_id}")

    if keys_to_delete:
        await redis.delete(*keys_to_delete)
