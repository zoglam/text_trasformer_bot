from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from config import BOT_TOKEN

from transform import Transform
from keyboards import Keyboard

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(msg: types.Message):
    start_msg = '*Change horizontal text to vertical*\nEnter sentence:'
    await msg.reply(start_msg, parse_mode="markdown")


@dp.message_handler(commands=["info"])
async def start_command(msg: types.Message):
    start_msg = 'Write text\nGet```\nt\ne\nx\nt```'
    await msg.reply(start_msg, parse_mode="markdown")


@dp.message_handler()
async def handle_message(msg: types.Message):

    global transform_obj
    transform_obj = Transform(msg.text)
    transform_obj.vertical()

    await msg.answer(
        str(transform_obj),
        parse_mode="markdown",
        reply_markup=Keyboard.inline_option_picker('Vertical')
    )


@dp.callback_query_handler()
async def answer(call):
    transform_obj.__getattribute__(call['data'].lower())()
    await bot.edit_message_text(
        chat_id=call['message']['chat']['id'],
        message_id=call['message']['message_id'],
        text=str(transform_obj),
        parse_mode="markdown",
        reply_markup=Keyboard.inline_option_picker(call['data'])
    )

if __name__ == '__main__':
    executor.start_polling(dp)
