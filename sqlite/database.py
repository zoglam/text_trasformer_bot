import sqlite3


class DB:

    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()
        try:
            self._prepare()
        except sqlite3.OperationalError as e:
            print(e)

    def _prepare(self):
        self.cursor.execute('''
            CREATE TABLE messages(
                chat_id INTEGER NOT NULL,
                msg_id INTEGER NOT NULL, 
                msg_text TEXT,
                PRIMARY KEY(chat_id, msg_id)
            )
        ''')
        self.conn.commit()

    def get(self, table: str, **params) -> list:
        try:
            return self.cursor.execute(f"""
                SELECT * FROM {table}
                WHERE {' and '.join([f'{k}={params[k]}' for k in params])}
            """).fetchall()
        except sqlite3.OperationalError as e:
            print(f'GET ERROR: {e}')
            return None

    def insert(self, table, **params) -> None:
        print(', '.join([f'{k}={params[k]}' for k in params]))
        try:
            self.cursor.execute(f"""
                INSERT INTO {table}({', '.join([f'"{k}"' for k in params])})
                VALUES(
                    {', '.join([f'"{params[k]}"' for k in params])}
                )
            """)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(f'INSERT ERROR: {e}')
