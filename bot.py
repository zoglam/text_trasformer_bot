from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(msg: types.Message):
    start_msg = '*Change horizontal text to vertical*\nEnter sentence:'
    await msg.reply(start_msg)


@dp.message_handler()
async def main(msg: types.Message):
    output_msg = f'```\n{trasform(msg)}```'
    await bot.send_message(
        msg.from_user.id,
        output_msg,
        parse_mode="markdown"
    )


def trasform(msg):
    words = msg.text.strip().split(' ')
    max_len = max(map(len, words))

    arr = [[' ' for j in range(len(words))] for i in range(max_len)]

    for i in range(max_len):
        for j in range(len(words)):
            try:
                output_msg[i][j] = words[j][i]
            except IndexError:
                continue

    return '\n'.join([' '.join(x) for x in arr])


if __name__ == '__main__':
    executor.start_polling(dp)
