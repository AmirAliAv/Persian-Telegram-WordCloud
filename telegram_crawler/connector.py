from telethon import TelegramClient


class Connector:
    def __init__(self, api_id, api_hash, phone_number):
        super().__init__()
        self.client = TelegramClient('crawler_session', api_id, api_hash)
        self.client.start(phone=phone_number)
