from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
import json


class ConfigLoader:
    @staticmethod
    def get_config():
        with open('config.json', 'r') as json_config_file:
            config = json.load(json_config_file)
        return config


class Connector:
    def __init__(self):
        super().__init__()
        self.config = ConfigLoader.get_config()
        self.client = TelegramClient(self.config['session_name'], self.config['api_id'], self.config['api_hash'])
        self.client.start(phone=self.config['phone_number'])

    def join_groups(self):
        groups_file = open(self.config['group_links'], "r")
        for group_id in groups_file:
            if len(group_id) != 0:
                try:
                    self.client(ImportChatInviteRequest(group_id))
                except:
                    pass