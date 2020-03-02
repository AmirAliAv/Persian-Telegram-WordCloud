from telethon import TelegramClient
import os


class Connector:
    def __init__(self, api_id, api_hash, phone_number):
        super().__init__()
        self.client = TelegramClient(os.path.dirname(os.path.realpath(__file__)) + '/crawler_session', api_id, api_hash)
        self.client.start(phone=phone_number)
