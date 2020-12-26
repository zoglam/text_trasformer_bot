from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from config import BOT_TOKEN

from transform import Transform
from keyboards import Keyboard

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
transform = Transform()


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
    transform.handle_new_message(msg.text)
    transform.line_by_line()
    await msg.answer(
        str(transform),
        parse_mode="markdown",
        reply_markup=Keyboard.inline_option_picker('Line_by_line')
    )


@dp.callback_query_handler()
async def answer(call):
    transform.edit_output_message(
        func=call['data'],
        chat_id=call['message']['chat']['id'],
        msg_id=call['message']['message_id'],
        msg_text=call['message']['text']
    )
    await bot.edit_message_text(
        chat_id=call['message']['chat']['id'],
        message_id=call['message']['message_id'],
        text=str(transform),
        parse_mode="markdown",
        reply_markup=Keyboard.inline_option_picker(call['data'])
    )

if __name__ == '__main__':
    executor.start_polling(dp)
    transform.db.conn.close()
