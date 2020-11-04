from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from config import BOT_TOKEN


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
    output_msg = f'```\n{trasform(msg)}```'
    await bot.send_message(
        msg.from_user.id,
        output_msg,
        parse_mode="markdown"
    )


def trasform(msg):
    if '\n' in msg.text:
        print(1)
        text = msg.text.strip().split('\n')
    else:
        print(2)
        text = msg.text.strip().split(' ')

    max_len = max(map(len, text))

    arr = [[' ' for j in range(len(text))] for i in range(max_len)]

    for i in range(max_len):
        for j in range(len(text)):
            try:
                arr[i][j] = text[j][i]
            except IndexError:
                continue

    return '\n'.join([' '.join(x) for x in arr])


if __name__ == '__main__':
    executor.start_polling(dp)
