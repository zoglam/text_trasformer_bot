import re

from sqlite.database import DB


class Transform(object):

    output_message = None
    words_list = None

    def __init__(self):
        self.db = DB()

    def __str__(self) -> str:
        return self.output_message

    @staticmethod
    def public_funcs() -> tuple:
        return ('Vertical', 'Square', 'Line_by_line')

    def _monospace_format(func):
        def wrapper(self):
            result = '\n'.join([' '.join(l) for l in func(self)])
            self.output_message = f'```\n{result}```'
        return wrapper

    @property
    def _words_count(self) -> int:
        return len(self.words_list)

    def handle_new_message(self, msg_text: str):
        self.words_list = re.findall(r'[a-zа-я0-9]+', msg_text.lower())

    def edit_output_message(self, func: str, chat_id, msg_id, msg_text) -> None:
        rows = self.db.get(table='messages', chat_id=chat_id, msg_id=msg_id)
        if not rows:
            msg_text = msg_text.replace(' ', '').replace('\n', ' ')
            self.db.insert(
                table='messages',
                chat_id=chat_id,
                msg_id=msg_id,
                msg_text=msg_text
            )
        else:
            _, _, msg_text = rows[0]
        self.handle_new_message(msg_text)
        self.__getattribute__(func.lower())()

    @_monospace_format
    def line_by_line(self) -> list:
        return self.words_list

    @_monospace_format
    def vertical(self) -> list:
        column_size = max(len(w) for w in self.words_list)
        output_arr = [[' ']*self._words_count for _ in range(column_size)]

        for column in range(self._words_count):
            for row, char in enumerate(self.words_list[column]):
                output_arr[row][column] = char

        return output_arr

    @_monospace_format
    def square(self) -> list:
        text_string = '*'.join(self.words_list)
        max_len = len(text_string) + (4 - len(text_string) % 4)
        text_string += ('*' * (4 - len(text_string) % 4))
        side_len = max_len // 4 + 1

        output_arr = [side_len * [' '] for _ in range(side_len)]

        operations_list = (
            lambda i, j: (i, j+1),
            lambda i, j: (i+1, j),
            lambda i, j: (i, j-1),
            lambda i, j: (i-1, j),
        )

        row, col, cursor = 0, 0, 0
        for oper_id in range(4):
            for _ in range(side_len-1):
                output_arr[row][col] = text_string[cursor]
                row, col = operations_list[oper_id](row, col)
                cursor += 1

        return output_arr
