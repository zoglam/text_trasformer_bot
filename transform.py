import re


class Transform(object):

    def __init__(self, msg_text: str):
        self.words_list = re.findall(r'[a-zа-я0-9]+', msg_text.lower())
        self.output_message = None

    def __str__(self) -> str:
        return self.output_message

    @classmethod
    def public_funcs(cls) -> tuple:
        return ('Vertical', 'Square')

    def _telegram_format(func):
        def wrapper(self):
            result = '\n'.join([' '.join(l) for l in func(self)])
            self.output_message = f'```\n{result}```'
        return wrapper

    @property
    def _words_count(self) -> int:
        return len(self.words_list)

    @_telegram_format
    def vertical(self) -> list:
        column_size = max(len(w) for w in self.words_list)
        output_arr = [[' ']*self._words_count for _ in range(column_size)]

        for column in range(self._words_count):
            for row, char in enumerate(self.words_list[column]):
                output_arr[row][column] = char

        return output_arr

    @_telegram_format
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
