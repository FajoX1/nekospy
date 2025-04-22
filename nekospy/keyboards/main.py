from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def edited_message_kb(
    message_link: str
) -> InlineKeyboardBuilder:
    
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        types.InlineKeyboardButton(
            text="Open message",
            url=message_link,
        )
    )

    return keyboard.as_markup()