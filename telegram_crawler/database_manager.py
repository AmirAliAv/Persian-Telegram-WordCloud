import sqlite3


class Database:
    def __init__(self, config: dict):
        super().__init__()
        self.db_file = config['database']  # type: str
        self.connection = sqlite3.connect(self.db_file)

    def fetch_all_query(self, query='''SELECT * FROM TelegramMessages'''):
        cursor = self.connection.cursor()
        cursor.execute(query, ())
        res = cursor.fetchall()
        cursor.close()
        return res

    def create_telegram_messages_table(self):
        c = self.connection.cursor()

        c.execute('''
                    CREATE TABLE IF NOT EXISTS `TelegramMessages` (
                        message_id BLOB,
                        body BLOB,
                        from_id BLOB,
                        fwd_from BLOB,
                        reply_to_msg_id BLOB,
                        date BLOB,
                        chat_name BLOB,
                        PRIMARY KEY(message_id, from_id, chat_name)
                    );
                ''')

        self.connection.commit()

    def create_pair_messages_table(self):
        c = self.connection.cursor()
        c.execute('''
                    CREATE TABLE IF NOT EXISTS `PairMessages` (
                        _id INTEGER,
                        msg_body BLOB,
                        reply_to_msg_body BLOB,
                        is_replied INTEGER,
                        language BLOB,
                        PRIMARY KEY(_id)
                    );
                ''')
        self.connection.commit()

    def insert_pair_message(self, _id, msg_body, reply_to_msg_body, is_replied, language):
        cursor = self.connection.cursor()
        cursor.execute(
            '''INSERT INTO PairMessages (_id, msg_body, reply_to_msg_body, is_replied, language) 
            VALUES (?, ?, ?, ?, ?)''',
            (_id, msg_body, reply_to_msg_body, is_replied, language))
        self.connection.commit()
        cursor.close()

    def insert_message(self, message_id, body, from_id, fwd_from, reply_to_msg_id, date, chat_name):
        cursor = self.connection.cursor()
        cursor.execute(
            '''INSERT INTO TelegramMessages (message_id, body, from_id, fwd_from, reply_to_msg_id, date, chat_name) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (message_id, body, from_id, fwd_from, reply_to_msg_id, date, chat_name))
        self.connection.commit()
        cursor.close()

    def get_message(self, chat_name: str, message_id: int):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                '''SELECT body FROM TelegramMessages WHERE message_id = ? AND chat_name = ?''',
                (message_id, chat_name))
            res = cursor.fetchone()
        except:  # means the messages is deleted
            cursor.close()
            return None

        cursor.close()
        return res[0]

    def get_all_messages(self):
        cursor = self.connection.cursor()
        for row in cursor.execute(
                '''SELECT body, reply_to_msg_id, chat_name FROM TelegramMessages ORDER BY date DESC''', ()):
            yield row
        cursor.close()
        return None

    def get_random_messages_of_chat(self, chat_name, limit=100):
        cursor = self.connection.cursor()
        cursor.execute(
            '''SELECT body FROM TelegramMessages WHERE chat_name = ? ORDER BY random() LIMIT ?''', (chat_name, limit))
        res = cursor.fetchall()
        cursor.close()
        return [r[0] for r in res]

    # def get_telegram_users(self):
    #     cursor = self.connection.cursor()
    #     try:
    #         return cursor.execute('''SELECT DISTINCT(from_id) from TelegramVoices''').fetchall()
    #     finally:
    #         cursor.close()
    #
    # def get_user_voices(self, user_id):
    #     cursor = self.connection.cursor()
    #     try:
    #         return cursor.execute('''SELECT document_id from TelegramVoices where from_id = (?)''', (user_id, )).fetchall()
    #     finally:
    #         cursor.close()