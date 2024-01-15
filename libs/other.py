from aiogram import Bot, types, F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.filters.callback_data import CallbackData
from aiogram.enums.chat_member_status import ChatMemberStatus

from libs.config import config

router = Router()

class CheckSubscribe(CallbackData, prefix='subscribe'):
    page: int

async def checkStatus(check):
    if check.status == ChatMemberStatus.MEMBER or check.status == ChatMemberStatus.ADMINISTRATOR or check.status == ChatMemberStatus.CREATOR: return True
    else: return False

@router.message(F.text)
async def get_base_message(message: types.Message, bot: Bot):
    user_id = message.chat.id
    if message.text == '/start':
        if await checkStatus(await bot.get_chat_member(config.get_channel(), user_id)):
            arr = await get_channels_config(user_id, bot)
            if len(arr) == 0:
                await bot.send_document(chat_id=user_id, document=FSInputFile(config.get_file()), caption='<b>Поздравляю!</b>✨\n\nВот твой файл, пользуйся им с умом! 😉')
            else:
                main_kb = InlineKeyboardMarkup(
                    inline_keyboard=arr
                )
                await message.answer(text='<b>Приветствую!</b>\n\n🔥Чтобы получить <b>"30 советов по темной и светлой психологии"</b>, тебе нужно подписаться на каналы наших партнеров партнеров:', reply_markup=main_kb)
        else:
            inline = InlineKeyboardBuilder()
            inline.add(InlineKeyboardButton(text="🥀 Подписаться на канал 🥀", url=config.get_url()))
            inline.add(InlineKeyboardButton(text="💫 Проверить подписку 💫", callback_data=CheckSubscribe(page=1).pack()))
            await message.answer(text='<b>Приветствую 👋</b>\n\n🔥Чтобы получить <b>"30 советов по темной и светлой психологии"</b>, тебе нужно подписаться на наш канал:', reply_markup=inline.as_markup())
        pass
    await message.delete()

@router.callback_query(CheckSubscribe.filter())
async def check_sub_handler(call: CallbackQuery, callback_data: CheckSubscribe, bot: Bot):
    user_id = call.message.chat.id
    page = int(callback_data.page)

    if page == 1:
        
        if await checkStatus(await bot.get_chat_member(config.get_channel(), user_id)):
            arr = await get_channels_config(user_id, bot)
            if len(arr) == 0:
                await bot.send_document(chat_id=user_id, document=FSInputFile(config.get_file()), caption='<b>Поздравляю!</b>✨\n\nВот твой файл, пользуйся им с умом! 😉')
            else:
                main_kb = InlineKeyboardMarkup(
                    inline_keyboard=arr
                )
                await call.message.answer(text='<b>Приветствую!</b>\n\n🔥 Чтобы получить <b>"30 советов по темной и светлой психологии"</b>, тебе нужно подписаться на каналы наших партнеров партнеров:', reply_markup=main_kb)
        else:
            inline = InlineKeyboardBuilder()
            inline.add(InlineKeyboardButton(text="🥀 Подписаться на канал 🥀", url=config.get_url()))
            inline.add(InlineKeyboardButton(text="💫 Проверить подписку 💫", callback_data=CheckSubscribe(page=1).pack()))
            await call.message.answer(text='❌ <b>Ты не подписан на канал!</b>\n\n🔥 Чтобы получить <b>"30 советов по темной и светлой психологии"</b>, тебе нужно подписаться на наш канал:', reply_markup=inline.as_markup())
    elif page == 2:
        arr = await get_channels_config(user_id, bot)
        if len(arr) == 0:
            await bot.send_document(chat_id=user_id, document=FSInputFile(config.get_file()), caption='<b>Поздравляю!</b>✨\n\nВот твой файл, пользуйся им с умом! 😉')
        else:
            main_kb = InlineKeyboardMarkup(
                inline_keyboard=arr
            )
            await call.message.answer(text='❌ <b>Ты не на все каналы подписался!</b>\n\n🔥 Чтобы получить <b>"30 советов по темной и светлой психологии"</b>, тебе нужно подписаться на каналы наших партнеров партнеров:', reply_markup=main_kb)
    await call.message.delete()

async def get_channels_config(user_id: int, bot: Bot) -> list:
    arr = []
    for i,j in config.get_channels().items():
        if not await checkStatus(await bot.get_chat_member(i, user_id)):
            arr.append([InlineKeyboardButton(text=j["Name"], url=j["Url"])])
    if len(arr) > 0:
        arr.append([InlineKeyboardButton(text="💫 Проверить подписк" + ("у" if len(arr) == 1 else "и") + " 💫", callback_data=CheckSubscribe(page=2).pack())])
    return arr