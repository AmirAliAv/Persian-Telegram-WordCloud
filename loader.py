import json


class ConfigLoader:
    @staticmethod
    def get_config():
        with open('config.json', 'r', encoding='utf-8') as json_config_file:
            config = json.load(json_config_file)
        return config
