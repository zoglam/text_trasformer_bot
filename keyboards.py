from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from transform import Transform


class Keyboard(object):

    @staticmethod
    def inline_option_picker(using_method:str=None) -> InlineKeyboardMarkup:

        options = Transform.public_funcs()
        buttons = (InlineKeyboardButton(text=option, callback_data=option)
                   for option in options if option != using_method)

        keyboard = InlineKeyboardMarkup()
        keyboard.add(*buttons)
        return keyboard
